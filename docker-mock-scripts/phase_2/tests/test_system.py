import sys
import distro

SYSTEM = sys.platform

try:
    assert SYSTEM != 'win32'
    assert SYSTEM != 'darwin'
    assert SYSTEM != 'linux'
    print('FAIL', file=sys.stdout)
except AssertionError:
    ID_NAME = distro.id()
    try:
        assert ID_NAME in {'debian', 'ubuntu'}
        print('PASS', file=sys.stdout)
    except AssertionError:
        print('FAIL', file=sys.stdout)

