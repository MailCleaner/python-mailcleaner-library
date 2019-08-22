#!/usr/bin/env python3
from enum import Enum

from sqlalchemy import orm, MetaData
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from mailcleaner.config import MailCleanerConfig

from mailcleaner.db.config import DBConfig

"""
Creation and initialization of database session.

@TODO
 - Add logs on MailCleaner for this package
 - Add tests for this package
"""


class DBPort(Enum):
    MASTER = 3306
    SLAVE = 3307


def is_master():
    """
    Determine if we're running code on a MailCleaner master or slave node.
    :return: True if it's a master, False otherwise
    """
    return MailCleanerConfig.get_instance().get_value("ISMASTER").upper() == "Y"


def get_db_connection_uri(database: str = DBConfig.DB_NAME.value, master: bool = is_master()) -> str:
    """
    Generate the database URLs for connecting SQLAlchemy.
    The MySQL URL connection should looks like dialect+driver://username:password@host:port/database
    :param database: the database to connect to
    :param master: boolean value to determine if we want to connect to master mysql instance or slave. Currently value is automatic
    by looking at via the ``is_master`` function.
    :return: a str containing the database URL
    """

    mysql_uri_connection = 'mysql+pymysql://' + DBConfig.DB_USER.value + ":" + DBConfig.DB_PASSWORD.value + "@"
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
