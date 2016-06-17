#! /usr/bin/env python

# -*- coding: utf-8 -*-

# The aim of this module is to make the installation of some dependancies easier

import sys
try :
    import pip
except ImportError:
    from scripts import getPip
    print("No module named pip - Error.")
    print("Installing Pip...")
    getPip.main()


def update():
    pip.main(['install','--upgrade','pip'])
    return


def install(package):
    pip.main(['install', package])
    return


if __name__ == '__main__':
    print("Updating pip...")
    update()
    print("Installing dependancies for ProjetS4...")
    install('Pillow')
    install('Numpy')
    install('Scipy')
    install('Theano')
    print("Done")

