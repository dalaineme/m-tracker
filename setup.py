"""Sets up our CLI"""

from setuptools import setup

setup(
    name="M-Tracker",
    version='0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        mtracker=cli:cli
    ''',
)
