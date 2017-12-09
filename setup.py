from setuptools import setup

setup(
    name='mesdossiers',
    packages=['mesdossiers'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy'
    ],
)