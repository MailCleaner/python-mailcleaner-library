from mailcleaner.dumper.DumpEximConfig import DumpEximConfig
import os.path
os.path.isfile = lambda path: path == '/path/to/testfile'
import filecmp


def test_dump_exim_stage2_config(session):
    DumpEximConfig().dump_exim_stage_2()
    assert (filecmp.cmp(
        "/usr/mailcleaner/etc/exim/exim_stage2.conf",
        "tests/unit/dumper/dumpEximConfig/EximStage2/exim.conf",
        shallow=False))
