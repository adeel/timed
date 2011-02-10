from setuptools import setup

setup(
  name='timed',
  version='0.2',
  description="command-line time tracking",
  long_description=open('README').read(),
  url='http://adeel.github.com/timed',
  author='Adeel Ahmad Khan',
  author_email='adeel@adeel.ru',
  py_modules=['timed', 'cmdapp'],
  entry_points={'console_scripts': ['timed = timed:main']},
  install_requires=['termcolor'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: Utilities',
  ],
  zip_safe=False,
)