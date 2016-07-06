#!/usr/bin/env python

from __future__ import print_function
import os
import subprocess
from it.polimi.server import fileUtils
import numpy

from it.polimi.utils import costManager


def clean_destination(destination_path, algo_list, phi_list, ni_range):
    result_dir_path = '{0}/results'.format(destination_path)  # in the destination path we create a rid called results
    fileUtils.check_path_and_clean(result_dir_path)

    for algorithm in algo_list:
        fileUtils.check_path_and_clean(result_dir_path + '/' + algorithm)
        for phi in phi_list:
            fileUtils.check_path_and_clean(result_dir_path + '/' + algorithm + '/' + str(phi))
            for i in ni_range:
                final_path = result_dir_path + '/' + algorithm + '/' + str(phi) + '/' + str(i)
                fileUtils.check_path_and_clean(final_path)


def launch(destination_path, algorithm, phi, ni, rand_seed):
    current_dir = os.getcwd()
    os.chdir(destination_path)
    file_to_run = './evaluate_' + algorithm + '_' + str(phi) + '_' + str(ni) + '_' + str(rand_seed) + '.run'
    subprocess.call(['./runAmpl', file_to_run])

    matlab_dir_path = destination_path + '/matlab'
    logs_path = destination_path + '/logs'
    fileUtils.check_file(matlab_dir_path, 'iwc.csv')
    fileUtils.check_file(matlab_dir_path, 'poa.csv')
    fileUtils.check_file(matlab_dir_path, 'time.txt')
    fileUtils.check_file(matlab_dir_path, 'iterations.csv')
    fileUtils.check_file(matlab_dir_path, 'potential.csv')
    fileUtils.check_file(logs_path, 'violations.txt')

    result_dir_path = '{0}/results'.format(destination_path)
    # fileUtils.CheckPathAndClean(resultDirPath)
    # fileUtils.CheckPathAndClean(resultDirPath+'/'+algorithm)
    # fileUtils.CheckPathAndClean(resultDirPath+'/'+algorithm+'/'+str(phi))
    final_path = result_dir_path + '/' + algorithm + '/' + str(phi) + '/' + str(ni)
    # fileUtils.CheckPathAndClean(finalPath)

    fileUtils.rename(matlab_dir_path + '/poa.csv', final_path + '/' + 'poa_' + str(rand_seed) + '.txt')
    fileUtils.rename(matlab_dir_path + '/iwc.csv', final_path + '/' + 'iwc_' + str(rand_seed) + '.txt')
    fileUtils.rename(matlab_dir_path + '/time.txt', final_path + '/' + 'time_' + str(rand_seed) + '.txt')
    fileUtils.rename(matlab_dir_path + '/iterations.csv', final_path + '/' + 'iterations_' + str(rand_seed) + '.txt')
    fileUtils.rename(matlab_dir_path + '/potential.csv', final_path + '/' + 'potential_' + str(rand_seed) + '.txt')
    fileUtils.rename(matlab_dir_path + '/cost.csv', final_path + '/' + 'cost_' + str(rand_seed) + '.txt')
    fileUtils.rename(matlab_dir_path + '/workloads.csv', final_path + '/' + 'workloads_' + str(rand_seed) + '.txt')
    fileUtils.rename(logs_path + '/violations.txt', final_path + '/' + 'violations_' + str(rand_seed) + '.txt')

    # fileUtils.rename(logs_path+'/resultValues.txt',finalPath+'/'+'resultValues_'+str(rand_seed)+'.txt')

    # debug
    # fileUtils.copyFile('poa.csv',matlab_dir_path,finalPath)
    # fileUtils.copyFile('iwc.csv',matlab_dir_path,finalPath)
    # fileUtils.copyFile('time.txt',matlab_dir_path,finalPath)
    # fileUtils.copyFile('/iterations.csv',matlab_dir_path,finalPath)
    # fileUtils.copyFile('/potential.csv',matlab_dir_path,finalPath)
    # fileUtils.copyFile('/cost.csv',matlab_dir_path,finalPath)
    # fileUtils.copyFile('/workloads.csv',matlab_dir_path,finalPath)
    # fileUtils.copyFile('/violations.txt',logs_path,finalPath)
    # fileUtils.rename(finalPath+'/poa.csv',finalPath+'/'+'poa_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/iwc.csv',finalPath+'/'+'iwc_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/time.txt',finalPath+'/'+'time_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/iterations.csv',finalPath+'/'+'iterations_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/potential.csv',finalPath+'/'+'potential_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/violations.txt',finalPath+'/'+'violations_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/cost.csv',finalPath+'/'+'cost_'+str(rand_seed)+'.txt')
    # fileUtils.rename(finalPath+'/workloads.csv',finalPath+'/'+'workloads_'+str(rand_seed)+'.txt')
    os.chdir(current_dir)


def launch_all(destination_path, algo_list, phi_list, ni_range, rand_seed_list):
    """
	Since many experiments might be executed this function iterates over the lists of parameters
	and launches the experiments
	"""

    clean_destination(destination_path, algo_list, phi_list, ni_range)
    for phiVal in phi_list:
        print('Phi value\t=\t{0}\t'.format(str(phiVal)))
        for ni_val in ni_range:
            print('Ni value\t=\t' + str(ni_val) + '\t')
            for alg in algo_list:
                print('Algorithm\t:\t' + alg + '\t')
                for randSeed in rand_seed_list:
                    print('RandSeed\t=\t' + str(randSeed) + '\n')
                    launch(destination_path, alg, phiVal, ni_val, randSeed)


def mean_time(destination_path, algorithm, phi, ni, randseed_list):
    full_path = destination_path + '/results/' + algorithm + '/' + str(phi) + '/' + str(ni)
    time_values = []
    for randSeed in randseed_list:
        f = open(full_path + '/time_' + str(randSeed) + '.txt', 'r')  # open the file
        line = f.readline()
        # discard the first line
        line = f.readline()
        words = line.split()
        if words[1] != 'secs':
            raise ValueError('Problems with time files')
        time_values.append(float(words[0]))
    return str(numpy.mean(time_values))


def mean_poa_and_iwc(index, destinationPath, algorithm, phi, ni, randSeedList):
    fullPath = destinationPath + '/results/' + algorithm + '/' + str(phi) + '/' + str(ni)
    poa_values = []
    for randSeed in randSeedList:
        with open(fullPath + '/' + index + '_' + str(randSeed) + '.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                # print(algorithm+'\t'+str(phi)+'\t'+str(ni)+'\t'+str(randSeed)+'\n')
                try:
                    poa_values.append(float(words[0]))
                except:
                    print(index + ' Infeasible!\n')

    if len(poa_values) > 0:
        return str(numpy.mean(poa_values))
    else:
        return '-'


def numInfeasibilities(index, destinationPath, algorithm, phi, ni, randSeedList):
    fullPath = destinationPath + '/results/' + algorithm + '/' + str(phi) + '/' + str(ni)
    poaValues = []
    infValues = []
    for randSeed in randSeedList:
        myFlag = True
        with open(fullPath + '/' + index + '_' + str(randSeed) + '.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                # print(algorithm+'\t'+str(phi)+'\t'+str(ni)+'\t'+str(randSeed)+'\n')
                try:
                    poaValues.append(float(words[0]))
                except:
                    infValues.append(1)
                    # if algorithm == 'threshold':
                    #	print(algorithm+' Infeasibility found!\n')
                    myFlag = False

        if myFlag:
            infValues.append(0)

    # print(len(infValues))
    # print('\n')
    return str(numpy.sum(infValues))


def meanViolations(destinationPath, algorithm, phi, ni, randSeedList):
    fullPath = destinationPath + '/results/' + algorithm + '/' + str(phi) + '/' + str(ni)
    violations = []
    for randSeed in randSeedList:
        with open(fullPath + '/violations_' + str(randSeed) + '.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                # print(algorithm+'\t'+str(phi)+'\t'+str(ni)+'\t'+str(randSeed)+'\n')
                # print(line)
                try:
                    violations.append(float(words[3]))
                except:
                    print('violations Infeasible!\n')
    if len(violations) > 0:
        return str(numpy.mean(violations))
    else:
        return '-'


# def mean_cost(destinationPath, algorithm, phi, ni, randSeedList):
#    fullPath = destinationPath + '/results/' + algorithm + '/' + str(phi) + '/' + str(ni)
#    cost = []
#    for randSeed in randSeedList:
#        with open(fullPath + '/cost_' + str(randSeed) + '.txt', 'r') as f:
#            for line in f.readlines():
#                words = line.split()
#                # print(algorithm+'\t'+str(phi)+'\t'+str(ni)+'\t'+str(randSeed)+'\n')
#                # print(line)
#                try:
#                    cost.append(float(words[3]))
#                except:
#                    print('cost Infeasible!\n')
#    if len(cost) > 0:
#        return str(numpy.mean(cost))
#    else:
#        return '-'


def mean_cost(destinationPath, algorithm, phi, ni, randSeedList):
    full_path = destinationPath + '/results/' + algorithm + '/' + str(phi) + '/' + str(ni)
    costs = []
    for randSeed in randSeedList:
        with open(full_path + '/cost_' + str(randSeed) + '.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                # print(algorithm+'\t'+str(phi)+'\t'+str(ni)+'\t'+str(randSeed)+'\n')
                # print(line)
                try:
                    # print(words[2])
                    # a = float(words[2])
                    costs.append(float(words[2]))
                except:
                    pass
    if len(costs) > 0:
        return str(numpy.mean(costs))
    else:
        return '-'


# questa funzione serve a verificare se tutte le IWC sono negative
def testIWC(strDestination, algoList, phiList, niRange, randSeedList):
    resultDirPath = strDestination + '/results'  #### fin qui.
    f = open(resultDirPath + '/IWC_Check.txt', 'w')
    f.write('Algorithm\tphi\tni\tIWC\n')
    f.write('___________________________________________________________________________________\n')
    for alg in algoList:
        for phiVal in phiList:
            for niVal in niRange:
                positive = check_iwc_positive(strDestination, alg, phiVal, niVal, randSeedList)
                f.write(alg + '\t' + str(phiVal) + '\t' + str(niVal) + '\t' + str(positive) + '\n')
    f.close()


def check_iwc_positive(destination_path, alg, phi_val, ni_val, randseed_list):
    full_path = destination_path + '/results/' + alg + '/' + str(phi_val) + '/' + str(ni_val)
    positive = True
    for randSeed in randseed_list:
        with open(full_path + '/iwc_' + str(randSeed) + '.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                # print(algorithm+'\t'+str(phi)+'\t'+str(ni)+'\t'+str(randSeed)+'\n')
                # print(line)
                try:
                    if float(words[0]) < 0:
                        positive = False
                        break
                except:
                    print('negative IWC!\n')
        if not positive:
            break
    return positive


def collect_results(destination_path, algo_list, phi_list, ni_range, rand_seed_list):
    fileUtils.check_path_and_clean(destination_path)
    result_dir_path = '{0}/results'.format(destination_path)
    fileUtils.check_path_and_clean(result_dir_path)
    join_results(algo_list, destination_path)
    f = open('{0}/finalResults.txt'.format(result_dir_path), 'w')

    f.write('Algorithm\tPhi\tNi\tTime\tPotential\tPoA\tIWC\tCost\n')
    f.write('___________________________________________________________________________________\n')
    for alg in algo_list:
        for phiVal in phi_list:
            for niVal in ni_range:
                time = mean_time(destination_path, alg, phiVal, niVal, rand_seed_list)
                poa = mean_poa_and_iwc('poa', destination_path, alg, phiVal, niVal, rand_seed_list)
                iwc = mean_poa_and_iwc('iwc', destination_path, alg, phiVal, niVal, rand_seed_list)
                potential = mean_poa_and_iwc('potential', destination_path, alg, phiVal, niVal, rand_seed_list)
                # numInfeas = numInfeasibilities('poa',destination_path,alg,phiVal,niVal,rand_seed_list)
                # iterations = meanPoAandIWC('iterations',destination_path,alg,phiVal,niVal,rand_seed_list)
                # violations = meanViolations(destination_path,alg,phiVal,niVal,rand_seed_list)
                cost = mean_cost(destination_path, alg, phiVal, niVal, rand_seed_list)
                f.write(alg + '\t' + str(phiVal) + '\t' + str(
                    niVal) + '\t' + time + '\t' + potential + '\t' + poa + '\t' + iwc + '\t' + cost + '\n')
    f.close()


# calcWorkFlow(destinationPath,algoList,phiList,niRange,randSeedList)

# f = open(resultDirPath+'/meanCosts.txt','w')
# f.write('Algorithm\tPhi\ti\tCost\t\tViolations\tIterations\tflow1\t\tflow2\tflow3\tDataTransfer\n')
# f.write('_______________________________________________________________________________________________________________________________\n')
# for alg in algoList:
# 	if alg == 'alg2_1':
# 		numIaaS =1
# 	if alg == 'alg2_2':
# 		numIaaS =2;
# 	if alg == 'alg2_3':
# 		numIaaS =3;
# 	for phiVal in phiList:
# 		for niVal in niRange:
# 			numInfeas = numInfeasibilities('poa',destinationPath,alg,phiVal,niVal,randSeedList)
# 			iterations = meanPoAandIWC('iterations',destinationPath,alg,phiVal,niVal,randSeedList)
# 			cost = meanCost(destinationPath,alg,phiVal,niVal,randSeedList)
# 			flow1 = workflow(1,destinationPath,alg,numIaaS,phiVal,niVal)
# 			flow2 = workflow(2,destinationPath,alg,numIaaS,phiVal,niVal)
# 			flow3 = workflow(3,destinationPath,alg,numIaaS,phiVal,niVal)
# 			dataTransfer = EgressCosts(destinationPath,alg,numIaaS,phiVal,niVal)
# 			f.write(alg+'\t\t'+str(phiVal)+'\t'+str(niVal)+'\t'+cost+'\t'+violations+'\t'+iterations+ '\t\t'+str(flow1)+'\t'+str(flow2)+'\t'+str(flow3)+'\t'+str(dataTransfer)+ '\n')
# f.close()

def calc_sync_cost(destination_path, algoList, phiList, niRange, randSeedList):
    resultDirPath = destination_path + '/results'
    f = open(resultDirPath + '/EgressCosts.txt', 'w')

    f.write('Algorithm\tPhi\tNi\tEgressCost\n')
    f.write('___________________________________________________________________________________\n')
    for alg in algoList:
        num_iaas = 0

        if alg == 'alg2_1':
            num_iaas = 1

        if alg == 'alg2_2':
            num_iaas = 2

        if alg == 'alg2_3':
            num_iaas = 3

        for phiVal in phiList:
            for niVal in niRange:
                data_transfer = egress_costs(destination_path, alg, num_iaas, phiVal, niVal, randSeedList)
                f.write(alg + '\t\t' + str(phiVal) + '\t' + str(niVal) + '\t' + str(data_transfer) + '\n')
    f.close()


def calc_synch_cost_graph(destinationPath, algoList, phiList, niRange, randSeedList):
    resultDirPath = destinationPath + '/results'
    f = open(resultDirPath + '/GraphCost.txt', 'w')

    f.write('Algorithm\tPhi\X\tEgressCost\n')
    f.write('___________________________________________________________________________________\n')
    for x in range(500, 50000, 500):
        for alg in algoList:
            num_iaas = 0
            if alg == 'alg2_1':
                num_iaas = 1
            if alg == 'alg2_2':
                num_iaas = 2
            if alg == 'alg2_3':
                num_iaas = 3
            for phiVal in phiList:
                data_transfer = []
                for niVal in niRange:
                    data_transfer.append(
                        egress_costs_param(destinationPath, alg, num_iaas, phiVal, niVal, randSeedList, x))
                if len(data_transfer) > 0:
                    # print(data_transfer)
                    # print('___________')
                    meanDataTransfer = str(numpy.mean(data_transfer))
                else:
                    meanDataTransfer = '0'

                f.write(alg + '\t\t' + str(phiVal) + '\t' + str(x) + '\t' + str(meanDataTransfer) + '\n')
    f.close()


def workflow(pType, destinationPath, alg, phiVal, niVal):
    fullPath = destinationPath + '/results/' + alg + '/' + str(phiVal) + '/' + str(niVal)
    D = 462  # number of bytes for record
    if pType == 1:
        sumIaaS1 = 0
        with open(fullPath + '/totalWorkloads_1' + '.txt', 'r') as f:
            for line in f.readlines():
                words = line.split()
                sumIaaS1 += float(words[0])
        dataFlow1 = sumIaaS1 * 30 * D
        return dataFlow1

    if pType == 2:
        if alg == 'alg2_1':
            return 0
        else:
            sumIaaS2 = 0
            with open(fullPath + '/totalWorkloads_2' + '.txt', 'r') as f:
                for line in f.readlines():
                    words = line.split()
                    sumIaaS2 += float(words[0])
            dataFlow2 = sumIaaS2 * 30 * D
            return dataFlow2

    if pType == 3:
        if alg in ['alg2_1', 'alg2_2']:
            return 0
        else:
            sumIaaS3 = 0
            with open(fullPath + '/totalWorkloads_3' + '.txt', 'r') as f:
                for line in f.readlines():
                    words = line.split()
                    sumIaaS3 += float(words[0])
            dataFlow3 = sumIaaS3 * 30 * D
            return dataFlow3


def egress_costs(destinationPath, alg, numIaaS, phiVal, niVal, seedList):
    # print('numIaaS: '+str(numIaaS))
    # print('alg: '+alg)
    # print('phi: '+str(phiVal))
    # print('ni: '+str(niVal))

    if numIaaS == 1:
        return 0
    else:
        fullPath = destinationPath + '/results/' + alg + '/' + str(phiVal) + '/' + str(niVal)
        vettEgrCosts = []
        sumIaaS1 = 0
        for seed in seedList:
            print('seed: ' + str(seed))
            filePath = fullPath + '/workloads_' + str(seed) + '.txt'
            print(filePath)
            with open(filePath, 'r') as f:
                for line in f.readlines():
                    if line != 'No apply':
                        words = line.split()
                        sumIaaS1 = 0
                        sumIaaS1 = float(words[0])
                        dataFlow1 = sumIaaS1 * 30
                        # print('dt1: '+str(dataFlow1))
                        # print('dt1: '+str(costManager.convertTB(dataFlow1*30)))
                        # print('AmazonCost: '+str(costManager.AmazonCost(dataFlow1)))
                        sumIaaS2 = float(words[1])
                        dataFlow2 = sumIaaS2 * 30
                        # print('dt2: '+str(dataFlow2))
                        # print('dt2: '+str(costManager.convertTB(dataFlow2*30)))
                        # print('GoogleCost: '+str(costManager.GoogleCost(dataFlow1)))

                        if numIaaS == 2:
                            vettEgrCosts.append(costManager.AmazonCost(dataFlow1) + costManager.GoogleCost(dataFlow2))
                        if numIaaS == 3:
                            sumIaaS3 = 0
                            sumIaaS3 = float(words[2])
                            dataFlow3 = sumIaaS3 * 30
                            vettEgrCosts.append(costManager.AmazonCost(2 * dataFlow1) + costManager.GoogleCost(
                                2 * dataFlow2) + costManager.AzureCost(2 * dataFlow3))

        if len(vettEgrCosts) > 0:
            return str(numpy.mean(vettEgrCosts))
        else:
            return '-'


def egress_costs_param(destination_path, alg, num_iaas, phiVal, niVal, seedList, Param):
    # print('num_iaas: '+str(num_iaas))
    # print('alg: '+alg)
    # print('phi: '+str(phiVal))
    # print('ni: '+str(niVal))
    factor = Param / 462.0
    if num_iaas == 1:
        return 0
    else:
        fullPath = destination_path + '/results/' + alg + '/' + str(phiVal) + '/' + str(niVal)
        vettEgrCosts = []
        sumIaaS1 = 0
        for seed in seedList:
            # print('seed: '+str(seed))
            filePath = fullPath + '/workloads_' + str(seed) + '.txt'
            # print(filePath)
            with open(filePath, 'r') as f:
                for line in f.readlines():
                    if line != 'No apply':
                        words = line.split()
                        sumIaaS1 = 0
                        sumIaaS1 = float(words[0])
                        dataFlow1 = sumIaaS1 * 30 * factor
                        # print('dt1: '+str(dataFlow1))
                        # print('dt1: '+str(costManager.convertTB(dataFlow1*30)))
                        # print('AmazonCost: '+str(costManager.AmazonCost(dataFlow1)))
                        sumIaaS2 = float(words[1])
                        dataFlow2 = sumIaaS2 * 30 * factor
                        # print('dt2: '+str(dataFlow2))
                        # print('dt2: '+str(costManager.convertTB(dataFlow2*30)))
                        # print('GoogleCost: '+str(costManager.GoogleCost(dataFlow1)))

                        if num_iaas == 2:
                            vettEgrCosts.append(costManager.AmazonCost(dataFlow1) + costManager.GoogleCost(dataFlow2))
                        if num_iaas == 3:
                            sumIaaS3 = 0
                            sumIaaS3 = float(words[2])
                            dataFlow3 = sumIaaS3 * 30 * factor
                            vettEgrCosts.append(costManager.AmazonCost(2 * dataFlow1) + costManager.GoogleCost(
                                2 * dataFlow2) + costManager.AzureCost(2 * dataFlow3))

        if len(vettEgrCosts) > 0:
            return numpy.mean(vettEgrCosts) / 30
        else:
            return 0


def join_results(algo_list, destination_path):
    for algo in algo_list:
        str_origin = "../" + algo + "_test_folder/results"
        str_destination = destination_path + '/results'
        # print(str_origin+'\n')
        # print(str_destination+'\n')
        fileUtils.copy_dir(str_origin, str_destination)


def calc_workflow(destinationPath, algoList, phiList, niRange, randSeedList):
    for alg in algoList:
        num_iaas = 0
        if alg == 'alg2_1':
            num_iaas = 1
        if alg == 'alg2_2':
            num_iaas = 2
        if alg == 'alg2_3':
            num_iaas = 3
        for phiVal in phiList:
            for niVal in niRange:
                split_workflow(destinationPath, alg, num_iaas, phiVal, niVal, randSeedList)


def split_workflow(destinationPath, alg, numIaaS, phiVal, niVal, randSeedList):
    fullPath = destinationPath + '/results/' + alg + '/' + str(phiVal) + '/' + str(niVal)

    if numIaaS == 1:
        f1 = open(fullPath + '/totalWorkloads_1.txt', 'w')

        arr1 = [[0 for x in range(len(randSeedList))] for x in range(24)]

        for seed, randSeed in enumerate(randSeedList):
            index1 = 0
            with open(fullPath + '/workloads_' + str(randSeed) + '.txt', 'r') as f:
                for i, line in enumerate(f.readlines()):
                    words = line.split()
                    print('i=' + str(i) + '\tline=' + line + '\n')
                    if i in range(1, 200, 2):
                        arr1[index1][seed] = float(words[0])
                        index1 += 1

        for row in arr1:
            f1.write("%s\n" % str(numpy.mean(row) * 3600))
        f1.close()

    if numIaaS == 2:
        f1 = open(fullPath + '/totalWorkloads_1.txt', 'w')
        f2 = open(fullPath + '/totalWorkloads_2.txt', 'w')
        arr1 = [[0 for x in range(len(randSeedList))] for x in range(24)]
        arr2 = [[0 for x in range(len(randSeedList))] for x in range(24)]

        for seed, randSeed in enumerate(randSeedList):
            index1 = 0
            index2 = 0
            with open(fullPath + '/workloads_' + str(randSeed) + '.txt', 'r') as f:
                for i, line in enumerate(f.readlines()):
                    words = line.split()
                    if i in range(1, 200, 3):
                        arr1[index1][seed] = float(words[0])
                        index1 += 1
                    if i in range(2, 200, 3):
                        arr2[index2][seed] = float(words[0])
                        index2 += 1

        for row in arr1:
            f1.write("%s\n" % str(numpy.mean(row) * 3600))
        f1.close()
        for row in arr2:
            f2.write("%s\n" % str(numpy.mean(row) * 3600))
        f2.close()

    if numIaaS == 3:
        f1 = open(fullPath + '/totalWorkloads_1.txt', 'w')
        f2 = open(fullPath + '/totalWorkloads_2.txt', 'w')
        f3 = open(fullPath + '/totalWorkloads_3.txt', 'w')
        arr1 = [[0 for x in range(len(randSeedList))] for x in range(24)]
        arr2 = [[0 for x in range(len(randSeedList))] for x in range(24)]
        arr3 = [[0 for x in range(len(randSeedList))] for x in range(24)]

        for seed, randSeed in enumerate(randSeedList):
            index1 = 0
            index2 = 0
            index3 = 0
            with open(fullPath + '/workloads_' + str(randSeed) + '.txt', 'r') as f:
                for i, line in enumerate(f.readlines()):
                    words = line.split()
                    if i in range(1, 200, 4):
                        arr1[index1][seed] = float(words[0])
                        index1 += 1
                    if i in range(2, 200, 4):
                        arr2[index2][seed] = float(words[0])
                        index2 += 1
                    if i in range(3, 200, 4):
                        arr3[index3][seed] = float(words[0])
                        index3 += 1

        for row in arr1:
            f1.write("%s\n" % str(numpy.mean(row) * 3600))
        f1.close()
        for row in arr2:
            f2.write("%s\n" % str(numpy.mean(row) * 3600))
        f2.close()
        for row in arr3:
            f3.write("%s\n" % str(numpy.mean(row) * 3600))
        f2.close()
