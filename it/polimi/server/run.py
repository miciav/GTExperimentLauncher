#!/usr/bin/env python

import os
import sys
import fileUtils
import executor

from it.polimi.utils import iniManager

# the script starts here

i_manager = iniManager.iniManager(os.getcwd())
i_manager.readIni()

algoList2Check = i_manager.get_algo_list()

algo = sys.argv[1]
if algo not in algoList2Check:
    sys.exit("Unknown algorithm " + sys.argv[1])

strOrigin = " ../../../BaseFiles/"  # directory of base files; those with the definition of algorithms
strDestination = "../../../../" + algo + "_test_folder"  # output directory

# checking existence of work-directory
fileUtils.check_path(strOrigin)

fileUtils.check_path_and_clean(strDestination)

print('Checks\tOk\n')

algoList = [algo]
phiList = i_manager.get_phi_list()

randSeedList = range(i_manager.get_num_repetitions()+1)

print("Algorithm to execute: " + sys.argv[1] + "\n")

print('current directory: ' + os.getcwd())
print('-----------------------------------------------------------------------------\n')
print('                                 Starting Test 1\n')
print('-----------------------------------------------------------------------------\n')

# creazione dei file
max_ni, min_ni, increasing_step = i_manager.get_ni_info()
niRange = range(max_ni, min_ni, -increasing_step)

fileUtils.create_launch_files(algoList, phiList, niRange, randSeedList, strOrigin, strDestination)

# muovo i file necessari al test
fileUtils.move_execution_files(strOrigin, strDestination)

print('Creation Environment\tOk\n')
# a questo punto tutti i file necessari sono stati salvati nella directory di test

print('Running the test...\n')

executor.launchAll(strDestination, algoList, phiList, niRange, randSeedList)
# executor.testIWC(strDestination,algoList,phiList,niRange,randSeedList)
# executor.collectResults(strDestination,algoList,phiList,niRange,randSeedList)

print('-----------------------------------------------------------------------------\n')
print('                                 Test 1 finished\n')
print('-----------------------------------------------------------------------------\n')


