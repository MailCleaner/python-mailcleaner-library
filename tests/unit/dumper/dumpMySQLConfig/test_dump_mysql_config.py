from mailcleaner.dumper.DumpMySQLConfig import DumpMySQLConfig
import os.path
os.path.isfile = lambda path: path == '/path/to/testfile'
import filecmp


def test_dump_mysql_config(session):
    DumpMySQLConfig().dump()
    assert (filecmp.cmp("/usr/mailcleaner/etc/mysql/my_master.cnf",
                        "tests/unit/dumper/dumpMySQLConfig/my_master.cnf",
                        shallow=False)
            and filecmp.cmp("/usr/mailcleaner/etc/mysql/my_slave.cnf",
                            "tests/unit/dumper/dumpMySQLConfig/my_slave.cnf",
                            shallow=False))
