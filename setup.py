__author__ = 'kyle'
from setuptools import setup

setup(
    name='raspy',
    version='0.5',
    description='Python library to interact with sensors and actuators using a Raspberry Pi.',
    url='http://github.com/kylecorry31/Raspy',
    author='Kyle Corry',
    author_email='kylecorry31@gmail.com',
    packages=['raspy'],
    install_requires=[
        "RPi.GPIO >= 0.5.0"
    ]
)
