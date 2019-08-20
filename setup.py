from setuptools import setup
import setuptools

setup(name='mailcleaner_db',
      version='0.1.1',
      description='API to connect to MailCleaners mailcleaner_db',
      url='https://github.com/MailCleaner/mailcleaner_db',
      author='Mentor Reka',
      author_email='reka@mailcleaner.net',
      license='GPL',
      packages=['mailcleaner_db', 'mailcleaner_db.config', 'mailcleaner_db.models'],
      zip_safe=False)