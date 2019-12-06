from setuptools import setup

setup(
    name='easyasyncio',
    version='5.2.4',
    packages=['easyasyncio'],
    url='https://github.com/RaphaelNanje/easyasyncio.git',
    license='MIT',
    author='Raphael Nanje',
    author_email='rtnanje@gmail.com',
    description='A library that makes asyncio simple',
    install_requires=[
        'logzero',
        'aiohttp',
        'requests',
        'easyfilemanager @ https://github.com/RaphaelNanje/easyfilemanager/archive/0.0.1.tar.gz#egg=easyfilemanager'
    ],
    python_requies='~=3.6'
)
