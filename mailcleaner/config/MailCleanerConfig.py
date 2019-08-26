import logging
import os


class MailCleanerConfig:
    """
    Singleton MailCleaner Configuration file parser.
    """

    instance = None
    dict = {}
    mailcleaner_conf_path = None

    def __init__(self):
        if "MC_CONFIG_PATH" in os.environ:
            self.mailcleaner_conf_path = os.environ['MC_CONFIG_PATH']
        else:
            self.mailcleaner_conf_path = "/etc/mailcleaner.conf"
        if not MailCleanerConfig.instance:
            MailCleanerConfig.instance = self
            MailCleanerConfig.dict = MailCleanerConfig.__get_all_values__(self)

    def __getattr__(self, name: str) -> str:
        return getattr(self.instance, name)

    def __repr__(self):
        items = ("%s=%r" % (k, v) for k, v in self.dict.items())
        return "<%s: {%s}>" % (self.__class__.__name__,
                               ', '.join(items)) + "\n"

    @staticmethod
    def get_instance() -> 'Config':
        """
        Get MailCleaner Config instance.
        :return: The MailCleanerConfig instance
        """
        """ Static access method. """
        if MailCleanerConfig.instance is None:
            MailCleanerConfig()
        return MailCleanerConfig.instance

    def __get_all_values__(self) -> dict:
        """
        Return all MailCleaner configuration
        :return:
        """
        dictionnary = {}
        if os.path.isfile(self.mailcleaner_conf_path):
            with open(self.mailcleaner_conf_path, 'r') as file:
                for line in file:
                    values = line.split('=')
                    dictionnary.update({values[0].strip(): values[1].strip()})
        else:
            raise FileNotFoundError
        return dictionnary

    def get_value(self, search: str) -> str:
        """
        Return the ``search`` entry of MailCleaner Configuration file
        :param search: the key to search
        :return: value associated to the key ``search``
        """
        return MailCleanerConfig.dict.get(search, '')

    def change_configuration(self, key: str, value: str) -> bool:
        """
        Replace a configuration value on /etc/mailcleaner.conf file if the key exists
        :param key: the key to search
        :param value: the value to replace
        :return: True if key was found and changes done, False otherwise
        """
        # First check if key exists in current dict
        if key not in self.dict:
            return False

        # Find and replace the key with the given value
        import fileinput
        changed = False
        if os.path.isfile(self.mailcleaner_conf_path):
            for line in fileinput.FileInput(self.mailcleaner_conf_path,
                                            inplace=1):
                line = line.rstrip()
                logging.debug("line: {}".format(line))
                if key in line:
                    line = str(key + " = " + value).rstrip("\n\r")
                    changed = True
                print(line, )
        else:
            raise FileNotFoundError

        MailCleanerConfig.dict = MailCleanerConfig.__get_all_values__(self)
        return changed

    def set_path(self, config_path: str) -> None:
        """
        Set the path of the MailCleaner configuration path.
        :param config_path: the new configuration path of MailCleaner configuration file
        :return: None
        """
        self.mailcleaner_conf_path = config_path
