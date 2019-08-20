from enum import Enum

from sqlalchemy import orm, MetaData
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from mailcleaner_config import Config

from mailcleaner_db.config import DBConfig

"""
@TODO
 - Add logs on MailCleaner for this package
 - Add tests for this package
"""


class DBPort(Enum):
    MASTER = 3306
    SLAVE = 3307


def get_db_connection_uri(database: str = DBConfig.DB_NAME.value, master: bool = True) -> str:
    """
    Generate the database URLs for connecting SQLAlchemy.
    The MySQL URL connection should looks like dialect+driver://username:password@host:port/database
    :param database: the database to connect to
    :param master: boolean value to determine if we want to connect to master mysql instance or slave
    :return: a str containing the database URL
    """

    mysql_uri_connection = 'mysql+pymysql://' + DBConfig.DB_USER.value + ":" + Config.get_instance().get_value('MYMAILCLEANERPWD') + "@"
    if master:
        mysql_uri_connection += ":" + str(DBPort.MASTER.value)
    else:
        mysql_uri_connection += ":" + str(DBPort.SLAVE.value)

    mysql_uri_connection += "/" + database
    return mysql_uri_connection


# Set database
base = declarative_base()
engine = db.create_engine(get_db_connection_uri())
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

metadata = MetaData()

from mailcleaner_db.models import User



# print("User (find_by_domain): {}".format(User.find_by_domain("toto.local")))
# print("User (find_by_username): {}".format(User.find_by_username("newton")))
# print("User (find_by_pref): {}".format(User.find_by_pref(8)))
