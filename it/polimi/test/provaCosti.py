#!/usr/bin/env python
from __future__ import print_function
from __future__ import print_function
from it.polimi.server import costManager
byteTB = 1099511627776 #numero bytes per TB
byteGB = 1073741824

print("Amazon")
#caso 1 - 1GB
print('costo caso 1 = '+str(costManager.AmazonCost(byteGB))+"\tdeve essere 0" ) #
#caso 2 - 5GB
print('costo caso 2 = '+str(costManager.AmazonCost(5*byteGB))+"\tdeve essere 0.36") #
#caso 3 -1TB
print('costo caso 3 = '+str(costManager.AmazonCost(1*byteTB))+"\tdeve essere 92.07") #
#caso 4 -10TB
print('costo caso 4 = '+str(costManager.AmazonCost(10*byteTB))+"\tdeve essere 921.51") #
#caso 5 -50TB
print('costo caso 5 = '+str(costManager.AmazonCost(50*byteTB))+"\tdeve essere 4403.11") #
#caso 6 -70TB
print('costo caso 6 = '+str(costManager.AmazonCost(70*byteTB))+"\tdeve essere 5836.71") #
#caso 7 -150TB
print('costo caso 7 = '+str(costManager.AmazonCost(150*byteTB))+"\tdeve essere 11571.11") #
#caso 8 -200TB
print('costo caso 8 = '+str(costManager.AmazonCost(200*byteTB))+"\tdeve essere 14131.11") #

print("Google")
#caso 1 - 1GB
print('costo caso 1 = '+str(costManager.GoogleCost(byteGB))+"\tdeve essere 0.05" ) #
#caso 2 - 10GB
print('costo caso 2 = '+str(costManager.GoogleCost(10*byteGB))+"\tdeve essere 0.5" ) #
#caso 3 - 100GB
print('costo caso 3 = '+str(costManager.GoogleCost(100*byteGB))+"\tdeve essere 5.0" ) #

print("Azure")
#caso 1 - 1GB
print('costo caso 1 = '+str(costManager.AzureCost(byteGB))+"\tdeve essere 0" ) #
#caso 2 - 5GB
print('costo caso 2 = '+str(costManager.AzureCost(5*byteGB))+"\tdeve essere 0") #
#caso 3 -1TB
print('costo caso 3 = '+str(costManager.AzureCost(1*byteTB))+"\tdeve essere 66.0312") #
#caso 4 -10TB
print('costo caso 4 = '+str(costManager.AzureCost(10*byteTB))+"\tdeve essere 663.228") #
#caso 5 -20TB
print('costo caso 5 = '+str(costManager.AzureCost(20*byteTB))+"\tdeve essere 1297.084") #

#caso 6 -50TB
print('costo caso 6 = '+str(costManager.AzureCost(50*byteTB))+"\tdeve essere 3198.652") #
#caso 7 -70TB
print('costo caso 7 = '+str(costManager.AzureCost(70*byteTB))+"\tdeve essere 4267.708") #
#caso 8 -150TB
print('costo caso 8 = '+str(costManager.AzureCost(150*byteTB))+"\tdeve essere 8543.932") #
#caso 8 -200TB
print('costo caso 9 = '+str(costManager.AzureCost(200*byteTB))+"\tdeve essere 10453.692") #

print("test1")
byte = 43452328772.2
data = byte/byteGB
print("Amazon GB transfer: " + str(data))
print('costo Amazon 1 = '+str(costManager.AmazonCost(byte))+"\tdeve essere 0" ) #

byte = 49166185677.8
data = byte/byteGB
print ('Google GB transfer: ' + str(data))
print('costo Google 1 = '+str(costManager.GoogleCost(byte))+"\tdeve essere 0" ) #

print("test2")

byte = 1213365289.75
data = byte/byteGB
print ("Amazon GB transfer: " + str(data))
print('costo Amazon 2 = '+str(costManager.AmazonCost(byte))+"\tdeve essere 0" ) #

byte = 46649062806.2
data = byte/byteGB
print ("Azure GB transfer: " + str(data))
print('costo Azure 2 = '+str(costManager.AzureCost(byte))+"\tdeve essere 0" ) #







