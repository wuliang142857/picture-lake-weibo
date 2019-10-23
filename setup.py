#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python
"""
@author: wuliang142857
@contact: wuliang142857@gmail.com
@date 2019/08/10 23:50
"""


import os.path
from setuptools import setup, find_packages
# https://stackoverflow.com/questions/25192794/no-module-named-pip-req
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    import pip._internal.download as download
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    import pip.download as download
here = os.path.dirname(__file__)
# parse_requirements() returns generator of pip.req.InstallRequirement objects
if os.path.exists(os.path.join(here, "requirements.txt")):
    install_reqs = parse_requirements(os.path.join(here, "requirements.txt"),
                                  session=download.PipSession())
else:
    install_reqs = []

setup(
    name='picture-lake-weibo',
    version='0.0.5',
    description='把新浪微博作爲圖床',
    long_description=open(os.path.join(here, "README.md"), encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='wuliang142857',
    author_email='wuliang142857@gmail.com',
    url='https://github.com/wuliang142857/picture-lake-weibo',
    classifiers=[
        'Programming Language :: Python :: 3.5'
    ],
    keywords='圖床',
    license='MIT',
    packages=find_packages(exclude=['tests', 'demo']),
    setup_requires=[],
    install_requires=[str(ir.req) for ir in install_reqs],
    extras_require={},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'picture-lake-weibo = picture_lake_weibo.PictureLakeWeibo:main'
        ]
    }
)
