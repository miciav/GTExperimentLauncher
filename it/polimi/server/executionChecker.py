#!/usr/bin/env python
from subprocess import check_output
import time
import os
from it.polimi.server import fileUtils
from it.polimi.server import executor
from it.polimi.utils import iniManager


def get_pid(name):
    """

    :type name: str
    """
    try:
        m = map(int, check_output(args).split())
        return m
    except:
        print('error in getting pid')
        return map(int, [0])

i_manager = iniManager.iniManager(os.getcwd())
i_manager.readIni()
server, p, username = i_manager.get_connection_settings()
command = "pgrep -u "+username+" screen"
pidMap = get_pid(command)

print('The processes in execution are {0}'.format(str(len(pidMap))))
while len(pidMap) > 1:
    time.sleep(15)
    pidMap = get_pid(command)
    print('The processes in execution are {0}'.format(str(len(pidMap))))


cwd, remote_path = i_manager.get_remote_path()

strOrigin = cwd + "/BaseFiles"
strDestination = remote_path + '/test_folder'
iwcCheckFile = 'IWC_Check.txt'
finalResultFile = 'finalResults.txt'
filePath = strDestination + '/results'

algoList = i_manager.get_algo_list()
phiList = i_manager.get_phi_list()

randSeedList = range(1, i_manager.get_num_repetitions()+1)

max_ni, min_ni, increasing_step = i_manager.get_ni_info()
niRange = range(max_ni, min_ni, -increasing_step)

print('Running the analysis...\n')
fileUtils.check_path(strOrigin)

fileUtils.check_path(strDestination)

fileUtils.check_path(filePath)

executor.collect_results(strDestination, algoList, phiList, niRange, randSeedList)
# executor.testIWC(strDestination,algoList,phiList,iRange, randSeedList)
# fileUtils.checkFile(filePath,iwcCheckFile)
fileUtils.check_file(filePath, finalResultFile)
