from __future__ import print_function

import numpy

from it.polimi.utils import costManager


def egress_costs_param(destination_path, alg, num_iaas, phi_val, ni_val, randseed_list, param):
    factor = param / 462.0
    if num_iaas == 1:
        return 0
    else:
        fullPath = destination_path + '/results/' + alg + '/' + str(phi_val) + '/' + str(ni_val)
        vett_egr_costs = []
        sumIaaS1 = 0
        for seed in randseed_list:
            filePath = fullPath + '/workloads_' + str(seed) + '.txt'
            with open(filePath, 'r') as f:
                for line in f.readlines():
                    if line != 'No apply':
                        words = line.split()
                        sumIaaS1 = 0
                        sumIaaS1 = float(words[0])
                        dataFlow1 = sumIaaS1 * 30 * factor
                        sumIaaS2 = float(words[1])
                        dataFlow2 = sumIaaS2 * 30 * factor
                        if num_iaas == 2:
                            vett_egr_costs.append(costManager.AmazonCost(dataFlow1) + costManager.GoogleCost(dataFlow2))
                        if num_iaas == 3:
                            sumIaaS3 = 0
                            sumIaaS3 = float(words[2])
                            dataFlow3 = sumIaaS3 * 30 * factor
                            vett_egr_costs.append(costManager.AmazonCost(2 * dataFlow1) + costManager.GoogleCost(
                                2 * dataFlow2) + costManager.AzureCost(2 * dataFlow3))

        if len(vett_egr_costs) > 0:
            return numpy.mean(vett_egr_costs) / 30
        else:
            return 0


def calc_sync_cost_graph(destination_path, algo_list, phi_list, ni_range, randseed_list):
    result_dir_path = destination_path + '/results'
    f = open(result_dir_path + '/GraphCost.txt', 'w')

    f.write('Algorithm\tPhi\X\tEgressCost\n')
    f.write('___________________________________________________________________________________\n')
    for x in range(500, 50000, 500):
        for alg in algo_list:
            num_iaas = 0
            if alg == 'alg2_1':
                num_iaas = 1
            if alg == 'alg2_2':
                num_iaas = 2
            if alg == 'alg2_3':
                num_iaas = 3
            for phiVal in phi_list:
                data_transfer = []
                for niVal in ni_range:
                    data_transfer.append(
                        egress_costs_param(destination_path, alg, num_iaas, phiVal, niVal, randseed_list, x))
                if len(data_transfer) > 0:
                    mean_data_transfer = str(numpy.mean(data_transfer))
                else:
                    mean_data_transfer = '0'

                f.write(alg + '\t\t' + str(phiVal) + '\t' + str(x) + '\t' + str(mean_data_transfer) + '\n')
    f.close()


strDestination = "../test_2_folder"

algoList = ['alg2_1', 'alg2_2', 'alg2_3']
phiList = [0.1, 0.3, 0.5]

iRange = range(1, 7)
randSeedList = range(1, 6)

print("Calculating Egress Costs...")
calc_sync_cost_graph(strDestination, algoList, phiList, iRange, randSeedList)
print("Analysis done.")
