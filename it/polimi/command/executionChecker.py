#!/usr/bin/env python
from subprocess import check_output
import time
from it.polimi.server import fileUtils
from it.polimi.server import executor


def get_pid(name):
    """

    :type name: str
    """
    try:
        m = map(int, check_output(["pidof", name]).split())
        return m
    except:
        return map(int, [0])


pidMap = get_pid("SCREEN")

print('The processes in execution are {0}'.format(str(len(pidMap))))
while len(pidMap) > 1:
    time.sleep(15)
    pidMap = get_pid("SCREEN")
    print('The processes in execution are {0}'.format(str(len(pidMap))))

strOrigin = "../../../BaseFiles/"
strDestination = "../../../../result_folder"
iwcCheckFile = 'IWC_Check.txt'
finalResultFile = 'finalResults.txt'
filePath = strDestination + '/results'

algoList = ['alg2_1', 'alg2_2', 'alg2_3']
phiList = [0.5]

randSeedList = range(1, 11)

iRange = range(1, 15, 1)

print('Running the analysis...\n')
fileUtils.check_path(strOrigin)

fileUtils.check_path(strDestination)

fileUtils.check_path(filePath)

executor.collect_results(strDestination, algoList, phiList, iRange, randSeedList)
# executor.testIWC(strDestination,algoList,phiList,iRange, randSeedList)
# fileUtils.checkFile(filePath,iwcCheckFile)
fileUtils.check_file(filePath, finalResultFile)
