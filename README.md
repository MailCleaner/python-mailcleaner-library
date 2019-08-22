# Python MailClenaer Package 

This package is a high level Python API for interacting with MailCleaner core components such as databases, dumpers etc.

For this, we use the recognized [SQLAlchemy](https://www.sqlalchemy.org/) ORM.

### Requirements

---

This library requires Python 3.4 and above. If you're unsure how to check what version of Python you're on, you can check it using the following:

> **Note:** You may need to use `python3` before your commands to ensure you use the correct Python path. e.g. `python3 --version`

```bash
python --version

-- or --

python3 --version
```

> **Note:** For installing Python 3: https://www.python.org/downloads/


### Installation

Until the package isn't available on a Python repository (such as [https://pypi.org/](pypi)), you have to go to package
sources and then run the installation thanks to the setuptools:

```shell
➜  mailcleaner: python3 setup.py install
```

### Development

For improving the current library, you need to first install dependencies with ``pip3``

```shell
➜  mailcleaner: pip3 install -r requirements.txt
```

> **Note:** For installing pip3: https://pip.pypa.io/en/stable/installing/


### Packages

---

#### mailcleaner.db

This package contains everything related to database interaction. You'll see for the moment two package:

- ``mailcleaner.db.models``: this package contains models for interacting with MailCleaner databases.
- ``mailcleaner.db.config``: who contains and should contains all configuration sutff relative to database.

#### mailcleaner.dumpers

This package contains all classes used for dumping MailCleaner services configurations files.

#### mailcleaner.config

This package contains MailCleaner Configuration class in order to deal with /etc/mailcleaner.conf file for example and other
Configuration stuff.

### Examples

---

Here are some examples of mailcleaner package use:

```python
    
    # -------------------------------------------------------------
    # Example of mailcleaner.db package
    # -------------------------------------------------------------
    from mailcleaner import get_db_connection_uri, DBConfig
    from mailcleaner.db.models import User, WWLists, MTAConfig
    
    # find, update and finally delete a database object
    user = User.find_by_id(12)
    user.username = "MySuperNewUsername"
    user.save()
    print(user) # <User: { domain = 'toto.local', id = 12, pref = 2, username = 'MySuperNewUsername'}>
    user.delete()
    # Every model on mailcleaner.db.models are printable thanks to the method __repr__ of BaseModel
    
    # get all users, the first and the last (usable by every Models)
    user.all()
    user.first()
    user.last()
    
    # get white-warn-black lists of a user
    # warning: relation doesn't exists between tables in MailCleaner.
    user = User.find_by_username_and_domain(username="tim.cook", domain="apple.ch")
    tim_cook_wwlists = WWLists.find_by_sender(sender=str(user.username + user.domain))
    
    # get database connection URI to the slave and master on mc_config db
    get_db_connection_uri(database=DBConfig.DB_NAME.value, master=False)
    get_db_connection_uri(database=DBConfig.DB_NAME.value, master=True)
    
    # get database connection URI to the slave and master on mc_spool db
    # mc_spool models doesn't exists, you should create them if needed
    get_db_connection_uri(database="mc_spool", master=False)
    get_db_connection_uri(database="mc_spool", master=True)
    
    # -------------------------------------------------------------
    # Example of mailcleaner.config package
    # -------------------------------------------------------------
    
    # MailCleanerConfig is a Singleton
    from mailcleaner.config import MailCleanerConfig
    
    mailcleaner_config = MailCleanerConfig.get_instance()
    client_id = mailcleaner_config.get_value("CLIENTID")
    host_id = mailcleaner_config.get_value("HOSTID")
    
    # -------------------------------------------------------------
    # Example of mailcleaner.dumpers package
    # -------------------------------------------------------------
    
    from mailcleaner.dumper import DumpEximConfig
    
    # Generate configuration content of exim_stage2.conf
    exim_config = DumpEximConfig()
    mta_config = MTAConfig.find_by_set_id_and_stage_id(set_id=1, stage_id=2)
    exim_stage2_config = exim_config.generate_config(template_config_src_file="etc/exim/exim_stage2.conf_template",
                                                     config_datas={"header_txt": mta_config.header_txt})
    print(exim_stage2_config) # Contains the exim_stage2.conf content
    
    # Dump the configuration of exim_stage2 in place. Will get the exim_stage2.conf_template and write
    # the exim_stage2.conf in place (replace current content).
    exim_config.dump_exim_stage_2()
```

### Tests
---

There are two kind of tests:

1) Unit
2) Integration

For running tests: ``python3 -m pytest -s --verbose tests/``

For running tests with coverage: ``python3 -m pytest  --cov=mailcleaner -s --verbose tests/``

We use pytest and [factoryboy](https://factoryboy.readthedocs.io/en/latest/introduction.html) for writting tests.

> **Note:** You may need to use `python3` before your commands to ensure you use the correct Python path. e.g. `python3 --version`


Examples of current tests:

```shell
➜  mailcleaner: python3 -m pytest -s --verbose tests/
=============================================== test session starts ================================================
platform linux -- Python 3.4.2, pytest-4.4.0, py-1.8.0, pluggy-0.12.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /root/mailcleaner/tests, inifile: pytest.ini
plugins: cov-2.7.1
collected 5 items

tests/integration/test_dump_fail2ban.py::test_dump_ssh_jail PASSED
tests/unit/test_mailcleaner_config.py::test_get_is_master PASSED
tests/unit/test_mailcleaner_config.py::test_get_and_check_dirs PASSED
tests/unit/test_mailcleaner_config.py::test_check_if_mc_config_file_exists PASSED
tests/unit/test_user_model.py::test_create_user PASSED

============================================= 5 passed in 0.18 seconds =============================================
```

### TO DO
---

* Add a flexible way to choose on which database instance to interact with. By default, every writes should be done on
the master of the cluster and every reads on the slave of the current host (where the code is ran). There is no ready solution
on SQLAlchemy however here is a begin with which we can work: https://stackoverflow.com/questions/12093956/how-to-separate-master-slave-db-read-writes-in-flask-sqlalchemy
* Because of fail2ban and not available python3.7 package under Debian Jessie, we used Python 3.4 but we should migrate the proejct to 3.7
(no issue should be encoutered)
*
