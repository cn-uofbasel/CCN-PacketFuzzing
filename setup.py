try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Packet_Fuzzing',
    version='0.1',
    description='Packet Fuzzing Software',
    author='Paul Hoeft, Tim Koenigl',
    packages=['Connection', 'Generation', 'Logger', 'Starter'],
    install_requires=['pyndn'],
)
