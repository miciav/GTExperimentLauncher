from __future__ import print_function
from it.polimi.server import executor

strDestination = "../test_2_folder"

algoList =['alg2_1', 'alg2_2', 'alg2_3']
phiList = [0.1, 0.3,0.5]

iRange = range(1,7)
randSeedList  = range(1,6)

print ("Collecting Results...")

executor.collect_results(strDestination,algoList,phiList,iRange,randSeedList)

print("Calculating Egress Costs...")
executor.calc_sync_cost(strDestination, algoList, phiList, iRange, randSeedList)
print ("Analysis done.")
