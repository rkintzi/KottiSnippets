import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.md')).read()

requires = [
        'kotti >= 0.8b1',
    ]

setup(name='KottiSnippets',
      version='0.2',
      description='KottiSnippets',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      package_data = {
          '': ['static/*', 'templates/*.pt', 'templates/forms/*.pt'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
#      test_suite="blog",
      entry_points = """\
      """,
      )

