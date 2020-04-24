#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='mailcleaner-library',
    version='1.0',
    description='MailCleaner Python Library',
    url='https://github.com/MailCleaner/python-mailcleaner-library',
    author='Mentor Reka',
    author_email='reka@mailcleaner.net',
    license='GPL',
    packages=find_packages(),
    install_requires=[
        'Jinja2>=2.11.2,<2.11.2',
        'SQLAlchemy>=1.3.16,<1.3.16',
        'PyMySQL>=0.9.3,<0.9.3',
        'factory-boy>=2.12.0,<2.12.0',
        'netifaces>=0.10.9,<0.10.9',
        'invoke>=1.4.1,<1.4.1',
        'click>=7.1.1,<7.1.1',
        'requests>=2.23.0,<2.23.0'
    ],
    scripts=['bin/fail2ban.py'],
    python_requires='>=3.7.7',
    zip_safe=False)
