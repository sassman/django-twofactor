# -*- coding: utf8 -*-

from setuptools import setup

version = '0.0.1'

setup(
    name='django-twofactor',
    version=version,
    author=('Mike Tigas', 'Sven Aßmann'),
    author_email='sven.assmann@lubico.biz',
    description='django auth integration with twofactor and googleauthentication',
    keywords='django auth googleauthenticator multifactor twofactor',
    url='https://github.com/sassman/django-twofactor',
    license='LICENSE.txt',
    packages=[
        'django_twofactor',
    ],
    long_description=open('README.mdown').read(),
    install_requires=[
        'oath>=1.0',
        'django>=1.4',
        'pycrypto'
    ]
)
