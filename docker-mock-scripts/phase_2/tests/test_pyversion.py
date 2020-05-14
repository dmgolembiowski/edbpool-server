import sys

SYSVERSION = sys.version_info

try:
    assert SYSVERSION >= (3, 8)
    print("PASS", file=sys.stdout)
except AssertionError:
    print("FAIL", file=sys.stdout)

