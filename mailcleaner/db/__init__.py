#!/usr/bin/env python3
from enum import Enum

from sqlalchemy import orm, MetaData
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

from sqlalchemy.ext.declarative import declarative_base

from mailcleaner.config import MailCleanerConfig

from mailcleaner.db.config import DBConfig

from os import environ
"""
Creation and initialization of database session.

@TODO
 - Add logs on MailCleaner for this package
 - Add tests for this package
"""


class DBPort(Enum):
    MASTER = 3306
    SLAVE = 3307
    PROXY = 3309


def is_master():
    """
    Determine if we're running code on a MailCleaner master or slave node.
    :return: True if it's a master, False otherwise
    """
    return MailCleanerConfig.get_instance().get_value(
        "ISMASTER").upper() == "Y"


def get_db_connection_uri(database: str = DBConfig.DB_NAME.value,
                          master: bool = is_master()) -> str:
    """
    Generate the database URLs for connecting SQLAlchemy.
    The MySQL URL connection should looks like dialect+driver://username:password@host:port/database
    :param database: the database to connect to
    :param master: boolean value to determine if we want to connect to master mysql instance or slave. Currently value is automatic
    by looking at via the ``is_master`` function.
    :return: a str containing the database URL
    """

    mysql_uri_connection = 'mysql+pymysql://' + DBConfig.DB_USER.value + ":" + DBConfig.DB_PASSWORD.value + "@"
    if "USE_SQL_PROXY" in environ:
        mysql_uri_connection += ":" + str(DBPort.PROXY.value)
    elif master:
        mysql_uri_connection += ":" + str(DBPort.MASTER.value)
    else:
        mysql_uri_connection += ":" + str(DBPort.SLAVE.value)

    mysql_uri_connection += "/" + database
    return mysql_uri_connection


engines = {
    'm_master':
    db.create_engine(
        'mysql+pymysql://' + DBConfig.DB_USER.value + ":" +
        DBConfig.DB_MASTER_PWD.value + "@" + DBConfig.DB_MASTER_IP.value + ":" +
        str(DBPort.MASTER.value) + "/mc_config",
        logging_name='m_master'),
    's_slave':
    db.create_engine(
        'mysql+pymysql://' + DBConfig.DB_USER.value + ":" +
        DBConfig.DB_PASSWORD.value + "@:" + str(DBPort.SLAVE.value) +
        "/mc_config",
        logging_name='s_slave'),
}


class RoutingSession(orm.Session):
    def get_bind(self, mapper=None, clause=None):
        if self._flushing:
            return engines['m_master']
        else:
            return engines['s_slave']

    _name = None

    def using_bind(self, name):
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name
        return s


# Set database
base = declarative_base()
#engine = db.create_engine(get_db_connection_uri())
#base.metadata.bind = engine
#if "USE_SQL_PROXY" in environ:
#else:
#    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
session = orm.scoped_session(orm.sessionmaker(class_=RoutingSession))
metadata = MetaData()
