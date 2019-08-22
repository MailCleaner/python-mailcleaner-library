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

    def set_path(self, config_path: str) -> None:
        """
        Set the path of the MailCleaner configuration path.
        :param config_path: the new configuration path of MailCleaner configuration file
        :return: None
        """
        self.mailcleaner_conf_path = config_path