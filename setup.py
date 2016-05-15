# -*- coding: utf-8 -*-

# The aim of this module is to make the installation of some dependancies easier

import pip


def install(package):
    pip.main(['install', package])


if __name__ == '__main__':
    install('Pillow')
    install('Numpy')
