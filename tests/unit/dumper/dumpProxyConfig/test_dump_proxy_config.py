from mailcleaner.dumper.DumpProxyConfig import DumpProxyConfig
import os.path
os.path.isfile = lambda path: path == '/path/to/testfile'
import filecmp
def test_dump_proxy_config(session):
    DumpProxyConfig().dump()
    assert(filecmp.cmp("/usr/mailcleaner/etc/proxysql/proxysql.conf", "tests/unit/dumper/dumpProxyConfig/original_dump.conf", shallow=False))
