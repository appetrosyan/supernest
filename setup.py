"""Setup code for the SSPR Package"""
import setuptools

with open("./README.md", "r") as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name='super-nest-a-p-petrosyan',
    version='0.1.0',
    author='Aleksandr Petrosyan',
    author_email='a-p-petrosyan@Yandex.ru',
    description='A wrapper for use of SSPR in \
nested sampling packages such as PolyChord and Multinest',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/a-p-petrosyan/sspr',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
