from setuptools import setup


setup(
    name='device',
    version='0.1.0',
    packages=['device'],
    package_dir={'device': '.'},
    install_requires=['rpi_ws281x', 'spidev'],
)