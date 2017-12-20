from setuptools import setup, find_packages

NAME = 'mesdossiers'
PACKAGES = find_packages(where='src')
INCLUDE_PACKAGE_DATA = True
INSTALL_REQUIRES = [
    'flask',
    'flask_sqlalchemy'
]

setup(
    name=NAME,
    packages=PACKAGES,
    package_dir={'': 'src'},
    include_package_data=INCLUDE_PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
)
