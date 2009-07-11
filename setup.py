from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name='Timed',
      version='0.1',
      description="command-line time tracking",
      long_description="command-line time tracking",
      author='Adeel Ahmad Khan',
      author_email='adeel2@umbc.edu',
      py_modules=['timed'],
      entry_points={'console_scripts': ['timed = timed:main']},
)