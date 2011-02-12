from distutils.core import setup

setup(
  name='timed',
  version='0.35',
  description="command-line time tracking",
  long_description=open('README').read(),
  url='http://adeel.github.com/timed',
  author='Adeel Ahmad Khan',
  author_email='adeel@adeel.ru',
  packages=['timed'],
  scripts=['bin/timed'],
  install_requires=['termcolor'],
  license='BSD',
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: Utilities',
  ]
)
