import os
import sh

from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.logger import shprint, info, info_main


class SpaceWayRecipe(PythonRecipe):
    version = #VERSION#
    url = 'file:///spaceway-{version}.tar.gz'

    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '')
    )

    depends = ['python3', 'pygame']
    python_depends = [
        'requests',
            'chardet',
            'idna',
            'urllib3',
            'certifi',
        'platformdirs',
        'packaging',
            'pyparsing'
    ]

    call_hostpython_via_targetpython = False
    install_in_hostpython = False

    def download_if_necessary(self):
        info_main('Downloading {}'.format(self.name))
        self.download()

    def download_file(self, url, target, cwd=None):
        if not url:
            return

        info('Downloading {} from {}'.format(self.name, url))

        if cwd:
            target = os.path.join(cwd, target)

        if os.path.exists(target):
            os.unlink(target)

        src = url.replace('file://', str(os.getenv('PATH_TO_PACKAGES')))
        shprint(sh.cp, src, target)


recipe = SpaceWayRecipe()
