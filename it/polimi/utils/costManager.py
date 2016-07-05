#!/usr/bin/env python
import numpy


def convertGB(data):
    # questa funzione calcola il numero di Gb
    byte_num = 1073741824  # numero di byte in un GB
    return data / byte_num


def convertTB(data):
    # questa funzione calcola il numero di TB
    byte_num = 1099511627776
    return data / byte_num


def TB2Byte(data):
    byte_num = 1099511627776
    return data * byte_num


def GB2Byte(data):
    byteNum = 1073741824
    return data * byteNum


def TB2GB(data):
    GB = 1024
    return data * GB


def GoogleCost(data):
    gb = convertGB(data)
    return numpy.ceil(gb) * 0.05


def AzureCost(data):
    gb = convertGB(data)
    tb = 1024

    if gb <= 5:
        return 0
    if gb > 5 and gb <= 10 * tb:
        return numpy.ceil(gb - 5) * 0.0648 + AzureCost(GB2Byte(5))
    if gb > 10 * tb and gb <= 50 * tb:
        return numpy.ceil(gb - 10 * tb) * 0.0619 + AzureCost(GB2Byte(10 * tb))
    if gb > 50 * tb and gb <= 150 * tb:
        return numpy.ceil(gb - 50 * tb) * 0.0522 + AzureCost(GB2Byte(50 * tb))
    if gb > 150 * tb and gb <= 500 * tb:
        return numpy.ceil(gb - 150 * tb) * 0.0373 + AzureCost(GB2Byte(150 * tb))
    else:
        return -1


def AmazonCost(data):
    tb = convertTB(data)
    gb = convertGB(data)

    if tb <= 10:
        return numpy.ceil(gb - 1) * 0.09
    if tb <= 50 and tb > 10:
        nextTb = (tb - 10)
        return (TB2GB(10) - 1) * 0.09 + numpy.ceil(TB2GB(nextTb)) * 0.085
    if tb <= 150 and tb > 50:
        nextTb = tb - 50
        return (TB2GB(10) - 1) * 0.09 + TB2GB(40) * 0.085 + numpy.ceil(TB2GB(nextTb)) * 0.07
    if tb <= 500 and tb > 150:
        nextTb = tb - 150
        return (TB2GB(10) - 1) * 0.09 + TB2GB(40) * 0.085 + TB2GB(100) * 0.07 + numpy.ceil(TB2GB(nextTb)) * 0.05
    else:
        return -1
