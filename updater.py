import os
import requests
from json import loads
from time import sleep
from sys import platform, exit, argv
from distutils.version import StrictVersion
from subprocess import Popen
from zipfile import ZipFile
from shutil import copyfile, copytree, rmtree


def is_available(config):
    try:
        r = requests.get('https://raw.githubusercontent.com/YariKartoshe4ka/Space-Way/master/config/config.json')

    except requests.exceptions.ConnectionError:
        return False

    else:
        version = loads(r.content)['version']

        if StrictVersion(config['version']) < StrictVersion(version):
            return version
        return False


def main(base_dir):
    os.mkdir(f'{base_dir}/tmp')
    r = requests.get(f"{config['rep_url']}/archive/{argv[1]}.zip")

    with open(f'{base_dir}/tmp/update.zip', 'wb') as file:
        file.write(r.content)

    with ZipFile(f'{base_dir}/tmp/update.zip', 'r') as file:
        file.extractall(f'{base_dir}/tmp/')

    if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
        rmtree(f'{base_dir}/assets/')

        copyfile(f'{base_dir}/tmp/Space-Way-{argv[1]}/main.py', f'{base_dir}/main.py')
        copytree(f'{base_dir}/tmp/Space-Way-{argv[1]}/assets/', f'{base_dir}/assets/')
        copyfile(f'{base_dir}/tmp/Space-Way-{argv[1]}/config/config.json', f'{base_dir}/config/config.json')
        copyfile(f'{base_dir}/tmp/Space-Way-{argv[1]}/icon.ico', f'{base_dir}/icon.ico')


    elif platform == 'win32':
        r = requests.get(f"{config['rep_url']}/releases/download/{argv[1]}/Space-Way-portable.exe")

        with open(f'{base_dir}/tmp/Space Way.exe', 'wb') as file:
            file.write(r.content)

        copyfile(f'{base_dir}/tmp/Space Way.exe', f'{base_dir}/Space Way.exe')
        copytree(f'{base_dir}/tmp/Space-Way-{argv[1]}/assets/', f'{base_dir}/assets/')
        copyfile(f'{base_dir}/tmp/Space-Way-{argv[1]}/config/config.json', f'{base_dir}/config/config.json')
        copyfile(f'{base_dir}/tmp/Space-Way-{argv[1]}/icon.ico', f'{base_dir}/icon.ico')
        

    rmtree(f'{base_dir}/tmp/')


if __name__ == '__main__':
    sleep(1)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    with open(f'{base_dir}/config/config.json', 'r') as file:
        config = loads(file.read())

    main(base_dir)

    if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
        Popen(['python3', f'{base_dir}/main.py'])

    elif platform == 'win32':
        Popen(['start', '', f'{base_dir}/Space Way.exe'])

    exit()
