from sqlalchemy import select

from config.config_parser import ConfigParser
from database import models
from database.database import DataBase
from parser.parser import Parser


def main():
    config = ConfigParser("config/config.ini")
    database = DataBase("database.sqlite3")
    parser = Parser(database, config)

    # database.delete_database()
    # database.create_all_tables()

    code = parser.auth("sobovyydv.19", "7*AGhjxz;kmvnlz")

    if code != '200':
        print("Авторизация не пройдена")
        exit(0)

    parser.get_user_id()
    print(parser.user_id)

    parser.get_csrf()
    print(parser.csrf)

    group_name = "П2-19"
    if database.select_query(select(models.Group), 2) is None:
        parser.get_groups()

    group_id = database.get_group(group_name)
    if database.select_query(select(models.Subject).where(models.Subject.group == group_id), 2) is None:
        parser.get_journal(group_name)

    semester = 5
    subject_name = "Иностранный язык"
    subject_id = database.get_subject((models.Subject.id,), subject_name, str(semester), group_name)[0]
    if database.select_query(select(models.Marks).where(models.Marks.group == group_id,
                                                        models.Marks.semester == semester,
                                                        models.Marks.subject == subject_id), 2) is None:
        parser.get_marks(group_name, semester, subject_name)

    print(database.get_all_groups())
    print(database.get_all_semesters("П2-19"))

    print(database.get_all_subjects("П2-19", 5))
    print(database.get_all_subjects("П2-19", 5, "text"))

    print(database.get_all_students("П2-19"))
    print(database.get_all_students("П2-19", "text"))

    print(database.get_group("П2-19"))
    print(database.get_group(245))


if __name__ == "__main__":
    main()
