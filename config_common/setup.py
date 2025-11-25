from setuptools import setup

setup(
    name='config_common',
    version='0.1.0',
    packages=['config_common'],
    package_dir={'config_common': '.'},
    install_requires=[
        'python-dotenv',
    ],
)