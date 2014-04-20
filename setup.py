from setuptools import setup, Extension, find_packages
import os.path


if os.path.exists(".this_is_a_checkout"):
    USE_CYTHON = True
else:
    # Don't depend on Cython in builds-from-sdist
    USE_CYTHON = False

DESC = """Compressed sorted sets -- a space-efficient, static database."""

LONG_DESC = (DESC + "\n"
             "Tools for creating and using the ``.zss`` file format,\n"
             "which allows for the storage of large, compressible\n"
             "data sets in a way that allows for efficient random access,\n"
             "range queries, and decompression. (Original use case:\n"
             "working with the multi-terabyte Google n-gram releases.)")

if USE_CYTHON:
    cython_ext = "pyx"
else:
    cython_ext = "c"
ext_modules = [
    Extension("zss._zss", ["zss/_zss.%s" % (cython_ext,)])
]
if USE_CYTHON:
    from Cython.Build import cythonize
    #import pdb; pdb.set_trace()
    ext_modules = cythonize(ext_modules)

setup(
    name="zss",
    version="0.0.0+dev",
    description=DESC,
    long_description=LONG_DESC,
    author="Nathaniel J. Smith",
    author_email="njs@pobox.com",
    url="https://github.com/njsmith/zss",
    classifiers =
      [ "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        ],
    packages=find_packages(),
    # This means, just install *everything* you see under zss/, even if it
    # doesn't look like a source file, so long as it appears in MANIFEST.in:
    include_package_data=True,
    # This lets us list some specific things we don't want installed, the
    # previous line notwithstanding:
    exclude_package_data={"": ["*.c", "*.pyx", "*.h", "README"],
                          # WTF this is ridiculous. We have to 'exclude' each
                          # data directory here so setuptools doesn't think we
                          # want to copy it, because you can't copy
                          # directories!  However everything *inside* the
                          # directories will still be copied. Which implicitly
                          # creates the directory. So basically this is how
                          # you say "yes please copy this directory (while
                          # pretending not to)".  This may get fixed at some
                          # point:
                          #   http://bugs.python.org/issue19286
                          "zss.tests": ["data",
                                        "data/broken-files",
                                        "data/http-test",
                                    ]},
    entry_points={
        "console_scripts": [
            "zss = zss.cmdline.main:entrypoint",
            ],
    },
    install_requires=["six", "requests", "docopt"],
    ext_modules=ext_modules,
)
