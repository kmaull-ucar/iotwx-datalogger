from setuptools import setup, find_packages

setup(
    name="iotwx2db",
    version=0.1,
    py_modules=['iotwx2db'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        iotwx2db=iotwx2db:cli
    ''',
)