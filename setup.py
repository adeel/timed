from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

f = open('README')
desc = f.read()
f.close()

setup(name='timed',
      version='0.11',
      description="command-line time tracking",
      long_description=desc,
      url='http://github.com/adeel/timed',
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
      include_package_data=True,
      data_files=[('', ['README'])],
      requirements=['PyYAML'],
      zip_safe=False,
)