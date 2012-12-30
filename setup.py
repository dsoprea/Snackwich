from setuptools import setup, find_packages
import sys, os

def pre_install():
    print("Verifying Snack availability.")
# TODO: Check for Newt, too.
    try:
        import snack
    except:
        print("Could not find snack. Please install the Newt or Snack "
              "packages before installing Snackwich.")
        return False

    return True

if not pre_install():
    sys.exit(1)

version = '1.3.13'

setup(name='snackwich',
      version=version,
      description="Configuration-based console UI forms.",
      long_description="Configuration-based Snack/Newt adaptation for easy and attractive console UI forms.",
      classifiers=['Development Status :: 3 - Alpha',
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
      packages=['snackwich'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

