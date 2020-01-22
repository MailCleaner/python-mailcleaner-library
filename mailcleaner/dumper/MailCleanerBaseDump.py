#!/usr/bin/env python3
import logging

from jinja2 import Environment, FileSystemLoader
from mailcleaner.config import MailCleanerConfig
import os.path


class MailCleanerBaseDump:
    """
    Base Component for dumpers. This class will take care of initializing Jinja2 engine, rendering the template and
    writing in place the new configuration file.
    """

    _mc_config = None

    def __init__(self):
        self._mc_config = MailCleanerConfig.get_instance()
        logging.basicConfig(
            filename='{}/{}/'.format(
                self._mc_config.get_value('VARDIR'),
                'log/mailcleaner/dumper.log'),
            level=logging.DEBUG)

    def __write_config(self, config_file_path: str, content: str):
        """
        Write the generated template ``content`` to ``config_file_path``
        :param content: configuration content to write
        :param config_file_path: the configuration file to create (or to replace) with content
        :return: True if the configuration dumps is successfull, False otherwise
        """
        try:
            with open(
                    file=config_file_path, mode="w", encoding="utf-8") as file:
                file.writelines(content)
            return True
        except Exception as e:
            logging.error("An exception occured while writing the {} file: \n{}") \
                .format(config_file_path, str(e))
            print("An exception occured while writing the {} file: \n{}") \
                .format(config_file_path, str(e))
            exit(code=255)
            return False

    def generate_config(self, template_config_src_file: str,
                        config_datas: dict) -> str:
        """
        Generate a new configuration based on the template file and the configurations datas.

        @TODO
            - Add a ``template_config_src_path`` and ``template_config_dst_path`` permitting users to extends
              the defaut behavior for example by specifying a different path than ``SRCDIR/etc/`` for config files but
              also to choose where the path of the destination config file.
            - Add a ``write_in_place`` argument which permits to choose to replace the destination config file
              (by writing in place) or not.

        :param template_config_src_file: Configuration raw template file. E.g: etc/fail2ban/fail2ban.conf_template
        :param config_datas: a dictionarry containing all variables used by the configuration templates such
               as conditionnal variables, dynamic variables, etc.
        :return: the configuration content if everything goes well or an empty str
        """
        logging.info("Start dumping conf ...")
        logging.info(
            "template_config_src_file: {}".format(template_config_src_file))
        logging.debug("config_datas: {}".format(config_datas))

        template_config_file_path = self._mc_config.get_value(
            'SRCDIR') + os.path.sep + template_config_src_file
        logging.debug(
            "template_config_file_path: {}".format(template_config_file_path))

        # Ensure that template config file exists
        if not os.path.exists(template_config_file_path):
            logging.error("Template file {} doesn't exists".format(
                template_config_file_path))
            print("Template file {} doesn't exists".format(
                template_config_file_path))
            exit(code=255)

        # Extract dir path for Jinja2 Environment
        DIR_PATH = os.path.dirname(os.path.abspath(template_config_file_path))
        logging.debug("DIR_PATH: {}".format(DIR_PATH))

        # Extract only the filename for rendering
        _, template_config_filename = os.path.split(template_config_file_path)
        logging.debug(
            "template_config_filename: {}".format(template_config_filename))

        try:
            # Generate config from the template thanks to Jinja2
            env = Environment(loader=FileSystemLoader(DIR_PATH))
            template_conf = env.get_template(template_config_filename)
            config_content = template_conf.render(config_datas)

            return config_content

        except Exception as e:
            logging.error("An exception occured during the dump of the config {} with the following error: \n{}")\
                .format(template_config_src_file, str(e))
            exit(code=255)

        return ""

    def dump_template(self,
                      template_config_src_file: str,
                      config_datas: dict,
                      destination_config_src_file: str = "") -> None:
        """
        Generate a new configuration based on the template file and the configurations datas. Also, dump (write) in place
        the new configuration file.
        :param template_config_src_file: Configuration raw template file. E.g: etc/fail2ban/fail2ban.conf_template
        :param config_datas: a dictionarry containing all variables used by the configuration templates such
               as conditionnal variables, dynamic variables, etc.
        :return: None
        """
        # Generate configuration data raw
        configuration_content = self.generate_config(template_config_src_file,
                                                     config_datas)

        # Write the configuration into the final configuration file
        template_config_file_path = self._mc_config.get_value(
            'SRCDIR') + os.path.sep
        if destination_config_src_file != "":
            template_config_file_path += destination_config_src_file
        else:
            template_config_file_path += template_config_src_file

        _, template_config_filename = os.path.split(
            template_config_file_path
        )  # Extract only the filename for rendering
        logging.debug(
            "template_config_filename: {}".format(template_config_filename))
        if "_template" in template_config_file_path:
            destination_config_file_path = template_config_file_path.replace(
                "_template", "")
        else:
            destination_config_file_path = template_config_file_path
        if self.__write_config(destination_config_file_path,
                               configuration_content):
            logging.info("New configuration successfuly writted to {}".format(
                destination_config_file_path))
        else:
            logging.info(
                "An error occured during the creation of the configuration {}"
                .format(destination_config_file_path))
