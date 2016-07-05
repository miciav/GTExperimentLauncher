from __future__ import print_function
from __future__ import print_function
from it.polimi.server import executor

strOrigin = "./BaseFiles"
strDestination = "../test_2_folder"
filePath = strDestination+'/results'

strDestination = "../test_2_folder"

algoList =['alg2_1','alg2_2', 'alg2_3']
phiList = [0.1, 0.3,0.5]

iRange = range(1,7)
randSeedList  = range(1,6)

print("Calculating Egress Costs...")
executor.calc_synch_cost_graph(strDestination,algoList,phiList,iRange,randSeedList)
print("Analysis done.")