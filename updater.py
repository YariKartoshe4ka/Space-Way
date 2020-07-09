from sys import platform, exit, argv
from os import mkdir, unlink
from time import sleep
from zipfile import ZipFile
from shutil import copyfile, rmtree, copytree
from subprocess import Popen
from requests import get
from packaging.version import parse


def check_software_updates(version, base_dir):
    try:
        r = get('https://raw.githubusercontent.com/YariKartoshe4ka/Space-Way/master/config/config.json')
    except:
        return
    else:
        remote_version = r.json().get('version', '0.0.0')

        if parse(version) < parse(remote_version):
            if platform == 'win32':
                Popen(f'start "" "{base_dir}/Updater.exe" {remote_version} {base_dir}', shell=True)
                exit()


def install_software_updates(remote_version, base_dir):
    mkdir(f'{base_dir}/tmp')

    if platform == 'win32':
        try:
            exe = get(f'https://github.com/YariKartoshe4ka/Space-Way/releases/download/{remote_version}/Space-Way-{remote_version}-portable.exe')
            zip = get(f'https://github.com/YariKartoshe4ka/Space-Way/archive/{remote_version}.zip')
        except:
            Popen(f'start "" "{base_dir}/Space Way.exe"', shell=True)
            exit()

        unlink(f'{base_dir}/Space Way.exe')
        with open(f'{base_dir}/Space Way.exe', 'wb') as file:
            file.write(exe.content)

        with open(f'{base_dir}/tmp/update.zip', 'wb') as file:
            file.write(zip.content)

        with ZipFile(f'{base_dir}/tmp/update.zip') as file:
            file.extractall(f'{base_dir}/tmp/')

        rmtree(f'{base_dir}/assets')
        unlink(f'{base_dir}/icon.ico')
        unlink(f'{base_dir}/config/config.json')

        copytree(f'{base_dir}/tmp/Space-Way-{remote_version}/assets', f'{base_dir}/assets')
        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/config/config.json', f'{base_dir}/config/config.json')
        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/icon.ico', f'{base_dir}/icon.ico')

        rmtree(f'{base_dir}/tmp')

        Popen(f'start "" "{base_dir}/Space Way.exe"', shell=True)
        exit()


if __name__ == '__main__':
    sleep(1)

    _, remote_version, base_dir = argv
    install_software_updates(remote_version, base_dir)
