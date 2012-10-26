from setuptools import setup, find_packages
import sys, os

version = '1.1.7'

setup(name='snackwich',
      version=version,
      description="Configuration-based console UI forms.",
      long_description="Configuration-based Snack/Newt adaptation for easy and attractive console UI forms.",
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: BSD License',
                   'Natural Language :: English',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Environment :: Console :: Newt'
                  ],
      keywords='console ui newt snack forms',
      author='Dustin Oprea',
      author_email='myselfasunder@gmail.com',
      url='https://github.com/dsoprea/Snackwich',
      license='New BSD',
      packages=['snackwich','example'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'setuptools'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

