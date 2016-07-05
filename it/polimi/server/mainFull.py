import os

import executor
import fileUtils

# the script starts here
strOrigin = " ../../../BaseFiles/"  # directory of base files; those with the definition of algorithms
strDestination = "../../../../test_folder"  # output directory

print('current directory: ' + os.getcwd())
print('-----------------------------------------------------------------------------\n')
print('                                 Starting Test 1\n')
print('-----------------------------------------------------------------------------\n')

# checking existence of work-directory
fileUtils.check_path(strOrigin)

fileUtils.check_path_and_clean(strDestination)

print('Checks\tOk\n')

# file creation
algoList = ['alg2', 'alg2_init_threshold', 'threshold']
phiList = [0.1, 0.3, 0.5]

randSeedList = range(1, 11)

niRange = range(100, 40, -5)

fileUtils.create_launch_files(algoList, phiList, niRange, randSeedList, strOrigin, strDestination)

# muovo i file necessari al test
fileUtils.move_execution_files(strOrigin, strDestination)

print('Creation Environment\tOk\n')
# a questo punto tutti i file necessari sono stati salvati nella directory di test

print('Running the test...\n')

executor.launch_all(strDestination, algoList, phiList, niRange, randSeedList)
executor.testIWC(strDestination, algoList, phiList, niRange, randSeedList)
executor.collect_results(strDestination, algoList, phiList, niRange, randSeedList)

print('-----------------------------------------------------------------------------\n')
print('                                 Test 1 finished\n')
print('-----------------------------------------------------------------------------\n')
