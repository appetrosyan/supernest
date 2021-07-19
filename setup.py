"""Setup code for the SSPR Package"""
import setuptools
import os

SHORT_DESCRIPTION = 'A wrapper for use of SSPR in \
nested sampling packages such as PolyChord and Multinest'
LONG_DESCRIPTION = SHORT_DESCRIPTION

with open("./README.md") as readme:
    LONG_DESCRIPTION = readme.read()

version="1.1.5"

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']

setuptools.setup(
    name='supernest',
    version=version,
    author='Aleksandr Petrosyan',
    author_email='a-p-petrosyan@yandex.ru',
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/a-p-petrosyan/sspr',
    install_requires=['anesthetic', 'numpy', 'matplotlib'],
    packages=setuptools.find_packages(),
    license='LGPLv3',
    python_requires='>=3.6',
    # I'd like to take this opportunity to rant about Python's abject
    # failure. Unfortunately, anyone with an IQ above their age, would
    # be able to identify the problems with using strings as
    # classifiers.

    # Problem 1: They're long. I keep getting complaints about this
    # not being PEP8 (a can of worms I'll open at another
    # time). Nobody thought that giving a less-descriptive string,
    # would have been better.

    # Problem 2: There's a ton of errors just waiting to be made., I
    # understand that there were some 'clever' people who thought
    # that, nobody is ever going to not put the space in the correct
    # place, but lo and behold, the official guideline on PyPI.org has
    # these typos.

    # Problem 3: There's a better way, that almost any programming
    # paradigm that supports strings can handle. It's called
    # variables. There aren't that many classifiers to cause name
    # collisions. Also, since many classifiers belong to the same
    # prefix, you could just create a class that encapsulates
    # them. Also, if you spell it wrong, your linter will complain
    # about it.

    # Problem 4: pip is not reliable. Just because it worked for you,
    # doesn't mean that it works in general. The side-effect ridden
    # setuptools, the frankly abysmal handling of the example code is
    # a good-enough incentive to improve bad designs. The fact that
    # nobody raised an issue, created a trivial pull request, and
    # fixed this, is good-enough proof that you should not rely on
    # `pip install X` not being an alias for `rm -rf /`.

    # Conclusions: Please think hard about infrastructure for a
    # language. First-off, use the language features. Secondly, think
    # about how your end users will work with your software. In fact,
    # just thinking would be sufficient. IF you ae packaging, consider
    # the alternatives. In my personal experience, numpy, scipy,
    # matplotlib and other 'de-facto' standards, are projects that
    # grew far beyond their original scope, are highly abused and
    # contain baffliningly terrible design choices. Your hand-rolled
    # solution is probably better. Same with PyPI.
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
    ]
)
