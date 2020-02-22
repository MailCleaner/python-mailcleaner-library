from mailcleaner.dumper.DumpEximConfig import DumpEximConfig
import os.path
os.path.isfile = lambda path: path == '/path/to/testfile'
import filecmp


def test_dump_exim_stage1_config(session):
    DumpEximConfig().dump_exim_stage_1()
    assert (filecmp.cmp(
        "/usr/mailcleaner/etc/exim/exim_stage1.conf",
        "tests/unit/dumper/dumpEximConfig/EximStage1/exim.conf",
        shallow=False))