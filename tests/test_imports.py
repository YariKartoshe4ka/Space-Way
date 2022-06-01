import sys
from importlib import reload

import pytest


@pytest.mark.parametrize('version', [
    (3, 5, 0),
    (3, 4, 10),
    (2, 7, 18)
])
def test_init(monkeypatch, version):
    import spaceway

    monkeypatch.setattr(sys, 'version_info', version)

    with pytest.raises(Exception):
        reload(spaceway)
