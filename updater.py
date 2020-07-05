import os
import requests
from json import loads
from time import sleep
from sys import platform, exit
from distutils.version import StrictVersion
from subprocess import Popen, DEVNULL
from zipfile import ZipFile
from shutil import copyfile, copytree, rmtree


def is_available(config):
    try:
        response = requests.get('https://raw.githubusercontent.com/YariKartoshe4ka/Space-Way/master/config/config.json')

    except requests.exceptions.ConnectionError:
        return False

    else:
        version = loads(response.content)['version']

        if StrictVersion(config['version']) < StrictVersion(version):
            return True
        return False


def main(base_dir):
    if platform == 'linux' or platform == 'linux2':
        os.mkdir(f'{base_dir}/tmp')
        r = requests.get(f"{config['rep_url']}/archive/master.zip")

        with open(f'{base_dir}/tmp/update.zip', 'wb') as file:
            file.write(r.content)

        with ZipFile(f'{base_dir}/tmp/update.zip', 'r') as file:
            file.extractall(f'{base_dir}/tmp/')

        rmtree(f'{base_dir}/assets/')

        copyfile(f'{base_dir}/tmp/Space-Way-master/main.py', f'{base_dir}/main.py')
        copytree(f'{base_dir}/tmp/Space-Way-master/assets/', f'{base_dir}/assets/')
        copyfile(f'{base_dir}/tmp/Space-Way-master/config/config.json', f'{base_dir}/config/config.json')

        rmtree(f'{base_dir}/tmp/')


if __name__ == '__main__':
    sleep(1)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f'{base_dir}/config/config.json', 'r') as file:
        config = loads(file.read())

    main(base_dir)

    Popen(['python3', f'{base_dir}/main.py'])
    exit()
