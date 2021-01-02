# OPERBOT - operbot (setuo.py)
#
# this file is placed in the public domain

from setuptools import setup

def readme():
    with open('README.rst') as file:
        return file.read()

setup(
    name='operbot',
    version='1',
    url='https://github.com/bthate/operbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="operbot",
    long_description=readme(),
    license='Public Domain',
    packages=["op", "operbot"],
    scripts=["bin/operbot", "bin/operctl", "bin/operudp"],
    zip_safe=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
