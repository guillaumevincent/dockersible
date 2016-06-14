from setuptools import find_packages
from setuptools import setup

setup(
    name='dockersible',
    version='0.0.1',
    author='Guillaume Vincent',
    author_email='guillaume@oslab.fr',
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=[
        'Click',
    ],
    entry_points="""
    [console_scripts]
    dockersible=dockersible.main:cli
    """,
    url='https://github.com/guillaumevincent/backup',
    description='script to backup docker images and volumes'
)
