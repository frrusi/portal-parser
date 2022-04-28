from configparser import SafeConfigParser


section_names = 'urls', 'codes', 'messages', 'headers'


class ConfigParser:
    def __init__(self, *file_names):
        parser = SafeConfigParser()
        found = parser.read(file_names, encoding="utf-8")
        if not found:
            raise FileNotFoundError('No config file found')
        for name in section_names:
            self.__dict__.update(parser.items(name))


