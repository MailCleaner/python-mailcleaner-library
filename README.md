# MailClenaer DB Python Package

The aim of this package is to provide a common API for interacting with MailCleaner databases in Python.

For this, we use the recognized [SQLAlchemy](https://www.sqlalchemy.org/) ORM.


TO DO:

* Add a flexible way to choose on which database instance to interact with. By default, every writes should be done on
the master of the cluster and every reads on the slave of the current host (where the code is ran). There is no ready solution
on SQLAlchemy however here is a begin with which we can work: https://stackoverflow.com/questions/12093956/how-to-separate-master-slave-db-read-writes-in-flask-sqlalchemy