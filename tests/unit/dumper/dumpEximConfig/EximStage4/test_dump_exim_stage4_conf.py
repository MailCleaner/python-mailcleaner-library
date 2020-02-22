from mailcleaner.dumper.DumpEximConfig import DumpEximConfig
import os.path
os.path.isfile = lambda path: path == '/path/to/testfile'
import filecmp


def test_dump_exim_stage4_config(session):
    DumpEximConfig().dump_exim_stage_4()
    assert (filecmp.cmp(
        "/usr/mailcleaner/etc/exim/exim_stage4.conf",
        "tests/unit/dumper/dumpEximConfig/EximStage4/exim.conf",
        shallow=False))
