#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='mailcleaner-library',
      version='1.0',
      description='MailCleaner Python Library',
      url='https://github.com/MailCleaner/python-mailcleaner-library',
      author='Mentor Reka',
      author_email='reka@mailcleaner.net',
      license='GPL',
      packages=find_packages(),
      install_requires=[
          'Jinja2>=2.10,<2.11', 'SQLAlchemy>=1.3.7,<1.4', 'PyMySQL>=0.9,<0.10',
          'factory-boy>=2.12,<2.13', 'netifaces>=0.10.9,<0.11',
          'invoke>=1.4.1,<1.5'
      ],
      zip_safe=False)