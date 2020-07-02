"""Setup code for the SSPR Package"""
import setuptools
import os

SHORT_DESCRIPTION = 'A wrapper for use of SSPR in \
nested sampling packages such as PolyChord and Multinest'
LONG_DESCRIPTION = SHORT_DESCRIPTION

with open("./README.md") as readme:
    LONG_DESCRIPTION = readme.read()

ver = "1.0.0"

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
    install_requires=['anesthetic', 'pypolychord', 'numpy', 'matplotlib'],
    packages=setuptools.find_packages(),
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'License:: OSI Approved:: GNU Lesser General Public License v3(LGPLv3)', # Genius
        'Natural Language:: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience:: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic:: Scientific/Engineering:: Physics',
        'Development Status :: 4 - Beta',
        'Environment :: Console'
    ]
)
