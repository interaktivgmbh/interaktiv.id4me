# coding=utf-8
from setuptools import setup, find_packages

version = '1.0'

setup(
    name='thokas.id4me',
    version=version,
    description="",
    long_description="",
    classifiers=[
        "Environment :: Web Environment",
        "Fraemwork :: Plone",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='',
    author_email='',
    url='',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['thokas', ],
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
    extras_require={'test': [
        'plone.app.testing',
    ]},
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """
      )
