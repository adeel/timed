from distutils.core import setup

setup(
  name='timed',
  version='0.4.1',
  description="command-line time tracker",
  url='http://adeel.github.com/timed',
  author='Adeel Ahmad Khan',
  author_email='adeel@adeel.ru',
  packages=['timed'],
  scripts=['bin/timed'],
  install_requires=['termcolor'],
  license='MIT',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Operating System :: POSIX',
    'Topic :: Utilities',
  ]
)
