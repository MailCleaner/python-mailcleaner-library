class MailCleanerRBL:

    dict = {}

    def __init__(self, file_path, rbls):
        for rbl in rbls:
            dict.append(self._read_rbl_file("{}.cf".format(file_path)))

    def _read_rbl_file(self, file_path):
        dictionnary = {}
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    values = line.split('=')
                    dictionnary.update({values[0].strip(): values[1].strip()})
        else:
            raise FileNotFoundError
        return dictionnary

    def check_valid_rbl_dnsname(self, file_path, rbl_name) -> bool:
        return True if self._read_rbl_file(file_path).dict.get(
            'dnsname', '') != '' else False

    def get_value(self, rbl, search: str) -> str:
        """
        Return the ``search`` entry of MailCleaner Configuration file
        :param rbl: rbl name in which to search entry
        :param search: the key to search
        :return: value associated to the key ``search``
        """
        return MailCleanerConfig.dict[rbl].get(search, '')