"""Setup code for the SSPR Package"""
import setuptools
import os

SHORT_DESCRIPTION = 'A wrapper for use of SSPR in \
nested sampling packages such as PolyChord and Multinest'
LONG_DESCRIPTION = SHORT_DESCRIPTION

with open("./README.md") as readme:
    LONG_DESCRIPTION = readme.read()

ver = "0.0.5"

if os.environ.get('CI_COMMIT_TAG'):
    ver = os.environ['CI_COMMIT_TAG']
   
setuptools.setup(
    name='super-nest-a-p-petrosyan',
    version=ver,
    author='Aleksandr Petrosyan',
    author_email='a-p-petrosyan@yandex.ru',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/a-p-petrosyan/sspr',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
