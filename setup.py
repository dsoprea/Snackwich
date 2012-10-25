from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='snackwich',
      version=version,
      description="Configuration-based console UI forms.",
      long_description="Configuration-based Snack/Newt adaptation for easy and attractive console UI forms.",
      classifiers=['Topic :: Software Development :: Libraries :: Python Modules',
                   'Environment :: Console :: Newt'
                  ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='console ui newt snack forms',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/Snackwich',
      license='New BSD',
      packages=find_packages('snackwich','example'),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
