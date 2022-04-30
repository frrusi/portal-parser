from sqlalchemy import select

from config.config_parser import ConfigParser
from database import models
from database.database import DataBase
from exceptions import Exceptions
from parser.parser import Parser
from utils.parser_utils import ParserUtils
from utils.secondary_utils import SecondaryUtils
from utils.security_utils import SecurityUtils


def main():
    config = ConfigParser("config/config.ini")
    parser_utils = ParserUtils(config)
    security_utils = SecurityUtils(config)
    secondary_utils = SecondaryUtils()
    exceptions = Exceptions(config)

    database = DataBase("database.sqlite3", config, parser_utils, security_utils, exceptions)
    parser = Parser(database, config, exceptions, parser_utils, security_utils, secondary_utils)

    # database.delete_database()
    # database.create_all_tables()

    code = parser.auth("sobovyydv.19", "7*AGhjxz;kmvnlz")
    exceptions.check_auth(code)

    parser.get_user_id()
    print(parser.user_id)

    parser.get_csrf()
    print(parser.csrf)

    group_name = "П3-19"
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
    print(database.get_all_semesters("П1-19"))

    print(database.get_all_subjects("П1-19", 5))
    print(database.get_all_subjects("П1-19", 5, "text"))

    print(database.get_all_students("П1-19"))
    print(database.get_all_students("П1-19", "text"))

    print(database.get_group("П1-19"))
    print(database.get_group(244))


if __name__ == "__main__":
    main()
