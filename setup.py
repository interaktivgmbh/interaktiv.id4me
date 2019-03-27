# coding=utf-8
from setuptools import setup, find_packages

version = '1.1.0'

setup(
    name='interaktiv.id4me',
    version=version,
    description="",
    long_description="",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        'Framework :: Plone :: 5.1',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Thomas Kastenholz',
    author_email='kastenholz@interaktiv.de',
    url='https://github.com/interaktivgmbh/interaktiv.id4me',
    license='GPL version 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['interaktiv', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'unittest2',
        'plone.testing',
        'plone.app.testing',
        'Products.BeakerSessionDataManager',
        'id4me-rp-client'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ]
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """
)
