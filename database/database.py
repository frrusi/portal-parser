import os
from itertools import chain
from typing import Union

import sqlalchemy.engine
from sqlalchemy import create_engine, MetaData, select, insert, update
from sqlalchemy.sql.functions import coalesce

from database import models
from utils.parser_utils import ParserUtils


class DataBase:
    def __init__(self, name, config, parser_utils, security_utils, exceptions):
        self.name = name
        self.metadata = MetaData()
        self.engine = create_engine(f'sqlite:///{name}')

        self.config = config
        self.parser_utils = parser_utils
        self.security_utils = security_utils
        self.exceptions = exceptions

    def delete_database(self):
        if os.path.exists(self.name):
            os.remove(self.name)

    def create_all_tables(self):
        if not os.path.exists(self.name):
            models.Base.metadata.create_all(self.engine)

    def engine_connect(self, query, isReturn=False) -> sqlalchemy.engine.ResultProxy | None:
        with self.engine.connect() as connection:
            if isReturn:
                return connection.execute(query)
            connection.execute(query)

    def select_query(self, query, return_type: int):
        self.exceptions.check_value_by_number_range((1, 2), return_type)
        with self.engine.connect() as connection:
            if return_type == 1:
                return connection.execute(query).fetchall()
            elif return_type == 2:
                return connection.execute(query).fetchone()

    def insert_query(self, table, *args):
        self.engine_connect(insert(table).values(args))

    def to_sql_query(self, table_object, table_name: str, index=None):
        with self.engine.connect() as connection:
            if index is None:
                table_object.to_sql(table_name, con=connection, if_exists='append', index=False)
            else:
                table_object.to_sql(table_name, con=connection, if_exists='append', index_label='id')

    def get_last_index(self, query):
        with self.engine.connect() as connection:
            try:
                index = int(sorted([index[0] for index in connection.execute(query).fetchall()])[-1]) + 1
            except IndexError:
                index = 0
        return index

    def get_all_groups(self):
        return list(chain.from_iterable(self.select_query(select(models.Group.group), 1)))

    def get_all_semesters(self, group: str):
        return list(chain.from_iterable(self.select_query(select(models.Subject.semester
                                                                 ).where(models.Subject.group == self.get_group(group)
                                                                         ).distinct(), 1)))

    def get_all_subjects(self, group: str, semester: int, return_value: str = None):
        select_query = models.Subject.subject if return_value == 'text' else models.Subject.id
        return list(chain.from_iterable(self.select_query(select(select_query
                                                                 ).where(models.Subject.group == self.get_group(group),
                                                                         models.Subject.semester == semester), 1)))

    def get_all_students(self, group: str, return_value: str = None):
        group_id = self.get_group(group)
        if return_value == "text":
            iterator = iter(list(chain.from_iterable(
                self.select_query(select(models.Students.name,
                                         models.Students.surname,
                                         coalesce(models.Students.patronymic, '')
                                         ).where(models.Students.group == group_id), 1))))
            return [' '.join(name).strip() for name in zip(iterator, iterator, iterator)]
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
                self.engine_connect(update(models.Authorized).where(models.Authorized.login == login
                                                                    ).values(password=hashed_password,
                                                                             date=date,
                                                                             time=time))
        return code

    def get_data(self, subject: str, semester: str):
        subject_id = self.select_query(select(models.Subject.id).where(models.Subject.subject == subject,
                                                                       models.Subject.semester == semester), 2)[0]

        return list(chain.from_iterable(self.select_query(select(models.Marks.lesson_date
                                                                 ).where(models.Marks.subject == subject_id,
                                                                         models.Marks.semester == semester,
                                                                         models.Marks.student == '0'), 1)))

    def get_marks(self, subject: str, semester: str):
        subject_id = self.select_query(select(models.Subject.id).where(models.Subject.subject == subject,
                                                                       models.Subject.semester == semester), 2)[0]
        return list(chain.from_iterable(self.select_query(select(models.Marks.mark
                                                                 ).where(models.Marks.subject == subject_id,
                                                                         models.Marks.semester == semester), 1)))

    def get_student_id(self, name, surname, patronymic=None):
        return self.select_query(select(models.Students.id).where(models.Students.name == name,
                                                                  models.Students.surname == surname,
                                                                  models.Students.patronymic == patronymic), 2)[0]

    def synchronization_groups(self, new_groups):
        date, time = ParserUtils.get_datetime_now()

        for group in new_groups:
            index = self.select_query(select(models.Group.id).where(models.Group.group == group), 2)

            if index is None:
                index = self.get_last_index(select(models.Group.id))
                print(index)
            else:
                index = index[0]

            stmt = sqlalchemy.dialects.sqlite.insert(models.Group
                                                     ).values(id=index,
                                                              group=str(group),
                                                              date=str(date),
                                                              time=str(time)
                                                              ).on_conflict_do_update(index_elements=[models.Group.id],
                                                                                      set_=dict(date=date, time=time))

            self.engine_connect(stmt)

    def synchronization_subjects_and_semesters(self, *args):
        date, time = ParserUtils.get_datetime_now()
        for subject in args[0]:
            group = self.get_group(int(subject[1]))
            subject_id = self.get_subject((models.Subject.id,), subject[2], subject[0], group)[0]

            if subject_id is None:
                subject_id = self.get_last_index(select(models.Subject.id))

            stmt = sqlalchemy.dialects.sqlite.insert(models.Subject).values(
                id=subject_id,
                semester=subject[0],
                group=subject[1],
                subject=subject[2],
                url=subject[3],
                date=str(date),
                time=str(time)
            )

            stmt = stmt.on_conflict_do_update(index_elements=[models.Subject.id],
                                              set_=dict(url=stmt.excluded.url, date=date, time=time))

            self.engine_connect(stmt)

        for student in args[1]:
            group_id = args[0][1]
            if len(student) == 2:
                student_id = self.get_student_id(student[0], student[1])
            elif len(student) == 3:
                student_id = self.get_student_id(student[0], student[1], student[2])

            if student_id is None:
                student_id = self.get_last_index(select(models.Students.id))

            stmt = sqlalchemy.dialects.sqlite.insert(models.Students).values(
                id=student_id,
                group=group_id,
                name=subject[0],
                surname=subject[1],
                patronymic=subject[2],
                date=str(date),
                time=str(time)
            )

            stmt = stmt.on_conflict_do_update(index_elements=[models.Students.id],
                                              set_=dict(date=date, time=time))

            self.engine_connect(stmt)

    # def synchronization_marks(self, new_data):
    #     date, time = ParserUtils.get_datetime_now()
    #     print(new_data)
    #     exit(1)
    #     for group in new_groups:
    #         index = self.select_query(select(models.Group.id).where(models.Group.group == group), 2)
    #
    #         if index is None:
    #             index = self.get_last_index(select(models.Group.id))
    #             print(index)
    #         else:
    #             index = index[0]
    #
    #         stmt = sqlalchemy.dialects.sqlite.insert(models.Group
    #                                                  ).values(id=index,
    #                                                           group=str(group),
    #                                                           date=str(date),
    #                                                           time=str(time)
    #                                                           ).on_conflict_do_update(index_elements=[models.Group.id],
    #                                                                                   set_=dict(date=date, time=time))
    #
    #         self.engine_connect(stmt)
