from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

setup(
  name='timed',
  version='0.12',
  description="command-line time tracking",
  long_description=open('README').read(),
  url='http://soundofemptiness.com/projects/timed',
  author='Adeel Ahmad Khan',
  author_email='adeel2@umbc.edu',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: Utilities',
  ],
  py_modules=['timed', 'cmdapp'],
  entry_points={'console_scripts': ['timed = timed:main']},
  zip_safe=False,
)