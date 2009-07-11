from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

f = open('README')
desc = f.read()
f.close()

setup(name='timed',
      version='0.2',
      description="command-line time tracking",
      long_description=desc,
      url='http://github.com/adeel/timed',
      author='Adeel Ahmad Khan',
      author_email='adeel2@umbc.edu',
      py_modules=['timed'],
      entry_points={'console_scripts': ['timed = timed:main']},
      include_package_data=True,
)