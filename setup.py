from setuptools import setup, find_packages
from json import load
from sys import platform


data_files = []

# Version of package
with open('spaceway/config/config.json', 'r') as file:
    version = load(file)['version']

# Adding requirements
install_requires = []
with open('requirements.txt', 'r') as file:
    for line in file:
        install_requires.append(line)

# Setup icon and link if platform is linux
if platform.startswith('linux'):
    data_files.extend((
        ('share/applications', ['setupfiles/Space Way.desktop']),
        ('share/icons', ['setupfiles/spaceway.svg'])
    ))


setup(
    name='spaceway',
    version=version,
    python_requires='>=3.6.0',

    author='YariKartoshe4ka',
    author_email='yaroslav.kikel.06@inbox.ru',

    url='https://github.com/YariKartoshe4ka/Space-Way',

    packages=find_packages(),

    entry_points={
        'console_scripts':
            ['spaceway = spaceway.main:main']
    },

    data_files=data_files,

    include_package_data=True,

    description='Space Way is arcade game about space, in which you must overcome the space path by flying around obstacles',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',

    install_requires=install_requires,

    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Games/Entertainment :: Arcade',
        'Operating System :: OS Independent'
    ],
)
