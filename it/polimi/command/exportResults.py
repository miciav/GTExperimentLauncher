#!/usr/bin/env python

from __future__ import print_function
import os
from it.polimi.server import fileUtils




"""
Credo che questo file non serva a niente.

"""
# the script starts here
strOrigin = "./BaseFiles" #qui ci sono i file di base che verranno modificati di volta in volta.
strDestination = "../test_folder"

print('current directory: '+os.getcwd())
print('-----------------------------------------------------------------------------\n')
print('                                 Starting result analysis Test 1\n')
print('-----------------------------------------------------------------------------\n')


#controllo esistenza directory di lavoro
fileUtils.check_path(strOrigin)

fileUtils.check_path(strDestination)

print('Checks\tOk\n')


#print('Creation Environment\tOk\n')
#a questo punto tutti i file necessari sono stati salvati nella directory di test

print('-----------------------------------------------------------------------------\n')
print('                                 Test 1 result analysis finished\n')
print('-----------------------------------------------------------------------------\n')


