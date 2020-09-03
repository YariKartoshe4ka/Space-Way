from sys import platform, exit, argv
from os import mkdir, unlink
from time import sleep
from zipfile import ZipFile
from shutil import copyfile, rmtree, copytree
from subprocess import Popen
from requests import get
from packaging.version import parse
from multiprocessing import Process, freeze_support


def gui(base_dir):
    import pygame
    import os

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption('Space Way')

    screen_rect = screen.get_rect()
    font = pygame.font.Font(f'{base_dir}/assets/updater/pixeboy.ttf', 28)

    bg = pygame.image.load(f'{base_dir}/assets/updater/background.bmp')
    bg_rect = bg.get_rect()

    tick = 0
    clock = pygame.time.Clock()

    loading = font.render('Updating .', True, (255, 255, 255))
    loading_rect = loading.get_rect()
    loading_rect.center = screen_rect.center

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if tick >= 30: tick = 0

        screen.fill((0, 0, 0))
        screen.blit(bg, bg_rect)
        screen.blit(loading, loading_rect)
        pygame.display.update()

        loading = font.render('Updating ' + '.' * (tick // 10 + 1), True, (0, 255, 255))

        tick += 1
        clock.tick(30)


def check_software_updates(version, base_dir):
    try:
        r = get('https://raw.githubusercontent.com/YariKartoshe4ka/Space-Way/master/config/config.json')
    except:
        return
    else:
        remote_version = r.json().get('version', '0.0.0')

        if parse(version) < parse(remote_version):
            if platform == 'win32':
                Popen(['start', '', f'{base_dir}/Updater.exe', remote_version, base_dir], shell=True)
                exit()

            elif platform in ['linux', 'linux2', 'darwin']:
                Popen(f'python3 "{base_dir}/updater.py" "{remote_version}" "{base_dir}"', shell=True)
                exit()


def install_software_updates(remote_version, base_dir, window):
    mkdir(f'{base_dir}/tmp')

    if platform == 'win32':
        try:
            exe = get(f'https://github.com/YariKartoshe4ka/Space-Way/releases/download/{remote_version}/Space-Way-{remote_version}-portable.exe')
            zip = get(f'https://github.com/YariKartoshe4ka/Space-Way/archive/{remote_version}.zip')
        except:
            window.terminate()
            Popen(['start', '', f'{base_dir}/Space Way.exe'], shell=True)
            exit()

        unlink(f'{base_dir}/Space Way.exe')
        with open(f'{base_dir}/Space Way.exe', 'wb') as file:
            file.write(exe.content)

        with open(f'{base_dir}/tmp/update.zip', 'wb') as file:
            file.write(zip.content)

        with ZipFile(f'{base_dir}/tmp/update.zip') as file:
            file.extractall(f'{base_dir}/tmp/')

        rmtree(f'{base_dir}/assets', ignore_errors=True)
        unlink(f'{base_dir}/icon.ico')
        unlink(f'{base_dir}/config/config.json')

        copytree(f'{base_dir}/tmp/Space-Way-{remote_version}/assets',
                 f'{base_dir}/assets',
                 ignore=lambda d, f: ['updater'] if 'updater' in f else [],
                 dirs_exist_ok=True)

        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/config/config.json', f'{base_dir}/config/config.json')
        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/icon.ico', f'{base_dir}/icon.ico')

        rmtree(f'{base_dir}/tmp')

        window.terminate()
        Popen(['start', '', f'{base_dir}/Space Way.exe', remote_version, base_dir], shell=True)
        exit()

    elif platform in ['linux', 'linux2', 'darwin']:
        try:
            zip = get(f'https://github.com/YariKartoshe4ka/Space-Way/archive/{remote_version}.zip')
        except:
            window.terminate()
            Popen(f'python3 "{base_dir}/main.py"', shell=True)
            exit()

        with open(f'{base_dir}/tmp/update.zip', 'wb') as file:
            file.write(zip.content)

        with ZipFile(f'{base_dir}/tmp/update.zip') as file:
            file.extractall(f'{base_dir}/tmp/')

        Popen(['pip3', 'install', '-r', f'{base_dir}/tmp/Space-Way-{remote_version}/requirements.txt']).wait()

        rmtree(f'{base_dir}/assets')
        rmtree(f'{base_dir}/scenes')
        unlink(f'{base_dir}/main.py')
        unlink(f'{base_dir}/icon.ico')
        unlink(f'{base_dir}/config/config.json')

        copytree(f'{base_dir}/tmp/Space-Way-{remote_version}/assets', f'{base_dir}/assets')
        copytree(f'{base_dir}/tmp/Space-Way-{remote_version}/scenes', f'{base_dir}/scenes')
        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/main.py', f'{base_dir}/main.py')
        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/icon.ico', f'{base_dir}/icon.ico')
        copyfile(f'{base_dir}/tmp/Space-Way-{remote_version}/config/config.json', f'{base_dir}/config/config.json')

        rmtree(f'{base_dir}/tmp')

        window.terminate()
        Popen(f'python3 "{base_dir}/main.py"', shell=True)
        exit()


if __name__ == '__main__':
    freeze_support()
    _, remote_version, base_dir = argv
    window = Process(target=gui, args=(base_dir,))
    window.start()
    install_software_updates(remote_version, base_dir, window)
    
