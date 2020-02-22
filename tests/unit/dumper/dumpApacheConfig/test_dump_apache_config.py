from mailcleaner.dumper.DumpApacheConfig import DumpApacheConfig
import os.path
os.path.isfile = lambda path: path == '/path/to/testfile'
import filecmp


def test_dump_apache_config(session):
    DumpApacheConfig().dump()
    assert (filecmp.cmp("/usr/mailcleaner/etc/apache/httpd.conf",
                        "tests/unit/dumper/dumpApacheConfig/httpd.conf",
                        shallow=False))
