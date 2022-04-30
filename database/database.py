import os
from itertools import chain
from typing import Union

from sqlalchemy import create_engine, MetaData, select, delete, insert, update
from sqlalchemy.sql.functions import coalesce

from database import models


class DataBase:
    def __init__(self, name, config, parser_utils, security_utils):
        self.name = name
        self.metadata = MetaData()
        self.engine = create_engine(f'sqlite:///{name}')

        self.config = config
        self.parser_utils = parser_utils
        self.security_utils = security_utils

    def delete_database(self):
        if os.path.exists(self.name):
            os.remove(self.name)

    def create_all_tables(self):
        if not os.path.exists(self.name):
            models.Base.metadata.create_all(self.engine)

    def select_query(self, query, return_type: int):
        with self.engine.connect() as connection:
            if return_type == 1:
                return connection.execute(query).fetchall()
            elif return_type == 2:
                return connection.execute(query).fetchone()
            else:
                raise ValueError("An invalid return_type value was entered. Possible values: [1, 2].")

    def insert_query(self, table, *args):
        with self.engine.connect() as connection:
            connection.execute(insert(table).values(args))

    def update_query(self, query):
        with self.engine.connect() as connection:
            connection.execute(query)

    def to_sql_query(self, table_object, table_name: str, index=None):
        with self.engine.connect() as connection:
            if index is None:
                table_object.to_sql(table_name, con=connection, if_exists='append', index=False)
            else:
                table_object.to_sql(table_name, con=connection, if_exists='append', index_label='id')

    def get_last_index(self, query):
        with self.engine.connect() as connection:
            try:
                index = int(connection.execute(query).fetchall()[-1][0]) + 1
            except IndexError:
                index = 0
        return index

    def get_all_groups(self):
        return list(chain.from_iterable(self.select_query(select(models.Group.group), 1)))

    def get_all_semesters(self, group: str):
        return list(chain.from_iterable(
            self.select_query(
                select(models.Subject.semester).where(models.Subject.group == self.get_group(group)).distinct(), 1)))

    def get_all_subjects(self, group: str, semester: int, return_value: str = None):
        select_query = models.Subject.subject if return_value == 'text' else models.Subject.id
        return list(chain.from_iterable(
            self.select_query(select(select_query
                                     ).where(models.Subject.group == self.get_group(group)
                                             ).where(models.Subject.semester == semester), 1)))

    def get_all_students(self, group: str, return_value: str = None):
        group_id = self.get_group(group)
        if return_value == 'text':
            iterator = iter(list(chain.from_iterable(
                self.select_query(
                    select(models.Students.name, models.Students.surname, coalesce(models.Students.patronymic, '')
                           ).where(models.Students.group == group_id), 1))))
            return [' '.join(name).strip() for name in zip(iterator, iterator, iterator)]
        else:
            return list(chain.from_iterable(self.select_query(select(models.Students.id
                                                                     ).where(models.Students.group == group_id), 1)))

    def get_group(self, group: Union[str, int]):
        if isinstance(group, int):
            select_query, where_query = models.Group.group, models.Group.id
        else:
            select_query, where_query = models.Group.id, models.Group.group
        return self.select_query(select(select_query).where(where_query == group), 1)[0][0]

    def get_subject(self, select_query: tuple, subject: str, semester, group):
        return self.select_query(select(*select_query).where(models.Subject.semester == semester,
                                                             models.Subject.subject == subject,
                                                             models.Subject.group == self.get_group(group)), 2)

    def delete_information_about_group(self, group: str):
        with self.engine.connect() as connection:
            for table in [models.Students, models.Subject, models.Marks]:
                connection.execute(delete(table).where(table.group == self.get_group(group)))

    def delete_marks_group(self, group: str, subject, semester):
        group_id = self.get_group(group)
        subject_id = self.get_subject((models.Subject.id,), subject, semester, group)[0]
        with self.engine.connect() as connection:
            connection.execute(delete(models.Marks).where(models.Marks.group == group_id,
                                                          models.Marks.subject == subject_id))

    def get_auth_data(self, login):
        return self.select_query(select(models.Authorized).where(models.Authorized.login == login), 2)

    def insert_auth_data(self, response, login, password):
        if str(code := self.parser_utils.get_auth_code(response)) == self.config.successful_code:
            hashed_password = self.security_utils.hash_password(password)
            last_index = self.get_last_index(select(models.Authorized.id))
            date, time = self.parser_utils.get_datetime_now()
            if self.get_auth_data(login) is None:
                self.insert_query(models.Authorized, last_index, login, hashed_password, date, time)
            else:
                self.update_query(update(models.Authorized).where(
                    models.Authorized.login == login
                ).values(password=hashed_password,
                         date=date,
                         time=time))
        return code

    def get_data(self, subject: str, semester: str):
        subject_id = self.select_query(select(models.Subject.id).where(models.Subject.subject == subject,
                                                                       models.Subject.semester == semester), 2)[0]

        return list(chain.from_iterable(self.select_query(select(models.Marks.lesson_date).where(
            models.Marks.subject == subject_id,
            models.Marks.semester == semester,
            models.Marks.student == '0'), 1)))

    def get_marks(self, subject: str, semester: str):
        subject_id = self.select_query(select(models.Subject.id).where(models.Subject.subject == subject,
                                                                       models.Subject.semester == semester), 2)[0]
        return list(chain.from_iterable(self.select_query(select(models.Marks.mark).where(
            models.Marks.subject == subject_id,
            models.Marks.semester == semester), 1)))
