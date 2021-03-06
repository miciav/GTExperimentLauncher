from __future__ import print_function

import numpy

from it.polimi.server.executor import collect_results
from it.polimi.utils import costManager

"""
This file must be updated .. it is useful for calculating the egress costs
"""


def egress_costs(destination_path, alg, num_iaas, phi_val, ni_val, randseed_list):
    if num_iaas == 1:
        return 0
    else:
        fullPath = destination_path + '/results/' + alg + '/' + str(phi_val) + '/' + str(ni_val)
        vettEgrCosts = []
        sumIaaS1 = 0
        for seed in randseed_list:
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
                        sumIaaS2 = float(words[1])
                        dataFlow2 = sumIaaS2 * 30

                        if num_iaas == 2:
                            vettEgrCosts.append(costManager.AmazonCost(dataFlow1) + costManager.GoogleCost(dataFlow2))
                        if num_iaas == 3:
                            sumIaaS3 = 0
                            sumIaaS3 = float(words[2])
                            dataFlow3 = sumIaaS3 * 30
                            vettEgrCosts.append(costManager.AmazonCost(2 * dataFlow1) + costManager.GoogleCost(
                                2 * dataFlow2) + costManager.AzureCost(2 * dataFlow3))

        if len(vettEgrCosts) > 0:
            return str(numpy.mean(vettEgrCosts))
        else:
            return '-'


def calc_sync_cost(destination_path, algo_list, phi_list, ni_range, randseed_list):
    result_dir_path = destination_path + '/results'
    f = open(result_dir_path + '/EgressCosts.txt', 'w')

    f.write('Algorithm\tPhi\tNi\tEgressCost\n')
    f.write('___________________________________________________________________________________\n')
    for alg in algo_list:
        num_iaas = 0

        if alg == 'alg2_1':
            num_iaas = 1

        if alg == 'alg2_2':
            num_iaas = 2

        if alg == 'alg2_3':
            num_iaas = 3

        for phiVal in phi_list:
            for niVal in ni_range:
                data_transfer = egress_costs(destination_path, alg, num_iaas, phiVal, niVal, randseed_list)
                f.write(alg + '\t\t' + str(phiVal) + '\t' + str(niVal) + '\t' + str(data_transfer) + '\n')
    f.close()


strDestination = "../test_2_folder"

algoList = ['alg2_1', 'alg2_2', 'alg2_3']
phiList = [0.1, 0.3, 0.5]

iRange = range(1, 7)
randSeedList = range(1, 6)

print("Collecting Results...")

collect_results(strDestination, algoList, phiList, iRange, randSeedList)

print("Calculating Egress Costs...")
calc_sync_cost(strDestination, algoList, phiList, iRange, randSeedList)
print("Analysis done.")
