#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab

""" A script to manage development tasks """
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

from os import path as p
from subprocess import call, check_call, CalledProcessError
from manager import Manager

manager = Manager()
BASEDIR = p.dirname(__file__)


def _upload():
    """Upload distribution files"""
    check_call(['twine', 'upload', p.join(BASEDIR, 'dist', '*')])


def _sdist():
    """Create a source distribution package"""
    check_call(p.join(BASEDIR, 'helpers', 'srcdist'))


def _wheel():
    """Create a wheel package"""
    check_call(p.join(BASEDIR, 'helpers', 'wheel'))


def _clean():
    """Remove Python file and build artifacts"""
    check_call(p.join(BASEDIR, 'helpers', 'clean'))


@manager.arg('where', 'w', help='Modules to check')
@manager.arg('strict', 's', help='Check with pylint')
@manager.command
def lint(where=None, strict=False):
    """Check style with linters"""
    args = 'pylint --rcfile=standard.rc -rn -fparseable ckanext'

    try:
        check_call(['flake8', where] if where else 'flake8')
        check_call(args.split(' ') + ['--py3k'])
        check_call(args.split(' ')) if strict else None
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def pipme():
    """Install requirements.txt"""
    exit(call('pip install -r requirements.txt'.split(' ')))


@manager.command
def release():
    """Package and upload a release"""
    try:
        _clean()
        _sdist()
        _wheel()
        _upload()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def build():
    """Create a source distribution and wheel package"""
    try:
        _clean()
        _sdist()
        _wheel()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def upload():
    """Upload distribution files"""
    try:
        _upload()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def sdist():
    """Create a source distribution package"""
    try:
        _sdist()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def wheel():
    """Create a wheel package"""
    try:
        _wheel()
    except CalledProcessError as e:
        exit(e.returncode)


@manager.command
def clean():
    """Remove Python file and build artifacts"""
    try:
        _clean()
    except CalledProcessError as e:
        exit(e.returncode)

if __name__ == '__main__':
    manager.main()
