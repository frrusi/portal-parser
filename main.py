from config.config_parser import ConfigParser
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

    database.delete_database()
    database.create_all_tables()

    parser.get_groups()
    parser.get_journal("П2-19")
    parser.get_marks("П2-19", 5, "Иностранный язык")

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
