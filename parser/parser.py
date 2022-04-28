import re

import numpy as np
import pandas as pd
import requests
from sqlalchemy import select

from database import models
from database.database import DataBase
from utils import parser_utils as pt
from utils import security_utils as st
from parser.parser_meta import ParserMeta
from config.config import Config


class Parser(metaclass=ParserMeta):
    def __init__(self, database: DataBase, config):
        self.config = config
        self.database = database

        self.session = requests.Session()
        self.session.headers = Config.get_headers_data(config.accept, config.user_agent)

        self.csrf = None
        self.user_id = None

    def auth(self, login: str, password: str):
        if (auth_data := self.database.get_auth_data(login)) is not None:
            return st.get_answer_check_password(auth_data[2], password, self.config)

        response = self.session.post(self.config.auth_url, Config.get_auth_data(login, password))
        return self.database.insert_auth_data(response, login, password, self.config)

    def reset_password_get_email(self, email: str):
        assert self.csrf is not None, "CSRF not found"

        response = self.session.post(self.config.recovery_url,
                                     Config.get_reset_password_data(email, self.csrf))

        pt.check_reset_password_message(pt.get_reset_password_message(self.session, self.config.recovery_url),
                                        self.config.enter_email_message,
                                        self.config.error_email_message)

        code = input("Введите код: ")
        pt.life_loop_thread(self.reset_password_get_code, True, response, code)

    def reset_password_get_code(self, response: requests.models.Response, code: str):
        assert self.csrf is not None, "CSRF not found"

        self.session.post(self.config.recovery_url,
                          Config.get_recovery_code_data(code, self.csrf),
                          cookies=response.cookies)

        pt.check_reset_password_message(pt.get_reset_password_message(self.session, self.config.recovery_url),
                                        self.config.enter_code_message,
                                        self.config.error_code_message)

    def get_user_id(self):
        tree = pt.get_tree(self.session, self.config.url)
        self.user_id = re.search(
            r'sender_id : \d*', str(tree.xpath('//script[contains(text(), "sender_id")]/text()'))
        ).group(0).split(':')[-1].strip()

    def get_csrf(self):
        tree = pt.get_tree(self.session, self.config.url)
        csrf = str(tree.xpath('//script[contains(text(),"csrf")]/text()'))
        self.csrf = re.search(r'csrf.*,', csrf).group(0)[:-1].split()[-1].replace("'", '')

    def change_avatar(self, path_image: str):
        response = self.session.post(self.config.upload_photo_url.format(id=self.user_id),
                                     files={'avatar_file': open(path_image, 'rb')})
        change_avatar = f'/{response.json()["files"][0]["file"]}'
        self.session.post(self.config.profile_data_url, {'change_avatar': change_avatar, 'csrf': self.csrf},
                          cookies=response.cookies)

    def change_email(self, email: str):
        assert self.csrf is not None, 'CSRF not found'

        self.session.post(self.config.profile_data_url,
                          Config.get_change_email_data(email, self.csrf))

    def change_password(self, password: str):
        self.session.post(self.config.profile_data_url,
                          Config.get_change_password_data(password, self.csrf))

    def get_full_info_about_auth_user(self):
        tree = pt.get_tree(self.session, self.config.user_url)
        return [check.strip() for check in tree.xpath('//div[@class="info"]/text()[normalize-space()]')]

    def get_groups(self):
        date, time, tree = pt.get_datetime_and_tree(self.session, self.config.groups_url.format(course='0'))
        last_course = int(tree.xpath('//select[@name="k"]/option[last()]/text()')[0])

        groups = []
        for course in range(1, last_course + 1):
            tree = pt.get_tree(self.session, self.config.groups_url.format(course=course))
            groups += [[group, date, time] for group in tree.xpath('//table/tr[position() > 1]/td[1]/text()')]

        groups = pd.DataFrame(groups, columns=['group', 'date', 'time'])
        self.database.to_sql_query(groups, 'groups')

    def get_journal(self, group: str):
        response = self.session.post(self.config.all_users_url, Config.get_search_data(group))

        url_journals = self.config.journals_url.format(id=response.json()["list"][0]["id"])
        group_id = self.database.select_query(select(models.Group.id).where(models.Group.group == group), 2)[0]
        pt.life_loop_thread(self.get_subjects, True, url_journals, group_id)

    def get_subjects(self, journal_url, group_id):
        date, time, tree = pt.get_datetime_and_tree(self.session, journal_url)
        first_journal_url = self.config.url + tree.xpath('//table/tr[2]/td[position() = last() - 1]/a')[0].get('href')

        thread_students = pt.life_loop_thread(self.get_students, False, first_journal_url, group_id)

        subjects = tree.xpath('//table/tr[position() > 1]/td[position() = 1 or position() = 2]/text()')
        urls = tree.xpath('//table/tr[position() > 1]/td[position() = 6]/a')

        index = self.database.get_last_index(select(models.Subject.id))

        subjects = np.unique(np.array([[subjects[index], group_id, subjects[index + 1].rstrip('.'),
                                        self.config.url + urls[index - index // 2].get('href'), date, time] for index in
                                       range(0, len(subjects), 2)]), axis=0)
        subjects = pd.DataFrame(subjects, columns=['semester', 'group', 'subject', 'url', 'date', 'time'],
                                index=range(index, index + len(subjects)))

        self.database.to_sql_query(subjects, 'subjects', '')
        thread_students.join()

    def get_students(self, url, group_id):
        date, time, tree = pt.get_datetime_and_tree(self.session, url)

        students = [name.split()[1:4] for name in tree.xpath(
            '(//span[@class="j_filter_by_fio"]/text() | //span[@class="j_filter_by_fio"]/strong/text())')]

        index = self.database.get_last_index(select(models.Students.id))

        students = pd.DataFrame(students, columns=['name', 'surname', 'patronymic'],
                                index=range(index, index + len(students)))
        students.insert(0, 'group', group_id)
        students['date'], students['time'] = date, time

        self.database.to_sql_query(students, 'students', '')

    def get_marks(self, group: str, semester: int, subject: str):
        group_id = int(self.database.get_group(group))
        subject_id, url = self.database.get_subject((models.Subject.id, models.Subject.url,), subject, semester, group)

        date, time, tree = pt.get_datetime_and_tree(self.session, url)
        students = self.database.get_all_students(group)
        index = self.database.get_last_index(select(models.Marks.id))

        dates = [date.strip() for date in tree.xpath('//a[@data-placement="left"]/text()')]

        length_dates = len(dates)
        if length_dates != 0:
            marks = [mark.text_content().strip() for mark in tree.xpath(
                f'//table[@class="fl_left scorestable"]/tbody/tr[position() <= {len(students)}]/td[position() > 1 and position() < last() - 4]')]

            marks = np.array([[index, group_id, students[index // length_dates % len(students)], subject_id, semester,
                               mark, dates[index % length_dates], date, time] for index, mark in
                              enumerate(marks, index)])

            marks = pd.DataFrame(marks, columns=['id', 'group', 'student', 'subject', 'semester', 'mark',
                                                 'lesson_date', 'date', 'time'], index=range(index, index + len(marks)))

            self.database.to_sql_query(marks, 'marks')
