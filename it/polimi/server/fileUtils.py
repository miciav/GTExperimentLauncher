import base64
import fileinput
import getpass
import os
import shutil
import sys


def file_copy(file_name, file_path, destination_path):
    """

    :param destination_path:
    :param file_name:
    :type file_path: str
    """
    full_file_name = file_path + '/' + file_name
    shutil.copy2(full_file_name, destination_path)  # file copy


def rename(orig_file_name, dest_file_name):
    """

    :param dest_file_name:
    :type orig_file_name: str
    """
    shutil.move(orig_file_name, dest_file_name)


def copy_dir(origin_path, destination_path):
    """

    :type origin_path: str
    :type destination_path: str
    """
    for item in os.listdir(origin_path):
        s = os.path.join(origin_path, item)
        d = os.path.join(destination_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)


def check_path_and_clean(destination):
    try:
        os.stat(destination)
        for the_file in os.listdir(destination):
            file_path = os.path.join(destination, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    except:
        os.mkdir(destination)


def check_path(dir_path):
    try:
        os.stat(dir_path)
    except:
        os.mkdir(dir_path)


def check_file(file_path, filename):
    """

    :type file_path: str
    """
    try:
        os.stat(file_path + '/' + filename)
    except:
        raise ValueError('No ' + filename + ' in destination directory ')


def check_local_file(file_path, fileName):
    try:
        os.stat(file_path + '/' + fileName)
    except:
        f = open(file_path + '/' + fileName, 'w')
        p = getpass.getpass('Password:')
        enc = base64.b64encode(p)
        f.write(enc + '\n')
        f.close()


def get_pass(filePath, fileName):
    check_local_file(filePath, fileName)
    f = open(filePath + '/' + fileName, 'r')
    p = f.readline().split()
    return base64.b64decode(p[0])


def change_static_definition(file_path, destination_path, phi, ni):
    def_filename = "static_definition"
    full_filename = '{0}/{1}.run'.format(file_path, def_filename)
    check_file(file_path, def_filename + ".run")
    destination_filename = destination_path + '/' + def_filename + '_' + str(phi) + '_' + str(ni) + '.run'
    shutil.copy2(full_filename, destination_path)  # file copy
    shutil.move(destination_path + '/' + def_filename + '.run', destination_filename)  # rename

    for line in fileinput.input(destination_filename, inplace=True):
        sys.stdout.write(line.replace('N{i in I}:= 70', 'N{i in I}:= ' + str(ni)))

    for line in fileinput.input(destination_filename, inplace=True):
        sys.stdout.write(line.replace('R{j in S, i in I}:=0.5', 'R{j in S, i in I}:=' + str(phi)))


def change_evaluate_file(filename, file_path, destination_path, phi, ni, randseed):
    full_filename = file_path + '/' + filename + ".run"
    check_file(file_path, filename + ".run")
    destination_filename = destination_path + '/' + filename + '_' + str(phi) + '_' + str(ni) + '_' + str(
        randseed) + '.run'
    shutil.copy2(full_filename, destination_path)  # file copy
    shutil.move(destination_path + '/' + filename + '.run', destination_filename)  # rename
    for line in fileinput.input(destination_filename, inplace=True):
        sys.stdout.write(line.replace('randseed 1', 'randseed ' + str(randseed)))
    for line in fileinput.input(destination_filename, inplace=True):
        sys.stdout.write(line.replace('include static_definition.run;',
                                      'include static_definition_' + str(phi) + '_' + str(ni) + '.run;'))


def create_launch_files(algo_list, phi_list, ni_range, randseed_list, str_origin, str_destination):
    for algo in algo_list:
        for phiVal in phi_list:
            for niVal in ni_range:
                change_static_definition(str_origin, str_destination, phiVal, niVal)
                for randSeed in randseed_list:  # inner loop
                    change_evaluate_file('evaluate_' + algo, str_origin, str_destination, phiVal, niVal, randSeed)
                # chanceEvaluateFile('evaluate_alg2_init_threshold',strOrigin,strDestination,phiVal,niVal,randSeed)


def move_execution_files(str_origin, str_destination):
    file_copy('algorithm2.run', str_origin, str_destination)
    file_copy('runAmpl', str_origin, str_destination)
    file_copy('ampl_console', str_origin, str_destination)
    file_copy('model.mod', str_origin, str_destination)
    file_copy('potential.mod', str_origin, str_destination)
    file_copy('define_sub_problems.run', str_origin, str_destination)
    file_copy('check_infeasible.run', str_origin, str_destination)
    file_copy('tot_vm_i.run', str_origin, str_destination)
    file_copy('check_capacity.run', str_origin, str_destination)
    file_copy('violations.run', str_origin, str_destination)
    file_copy('util', str_origin, str_destination)
    # creazione dir Data
    check_path_and_clean(str_destination + '/data')
    file_copy('model-1-i-100-j-100-k-1-ixj-shuffle.dat', str_origin, str_destination + '/data')
    file_copy('model-2-i-100-j-100-k-2-ixj-shuffle.dat', str_origin, str_destination + '/data')
    file_copy('model-3-i-100-j-100-k-3-ixj-shuffle.dat', str_origin, str_destination + '/data')
    file_copy('24hours.dat', str_origin, str_destination + '/data')
    file_copy('model-lambda.dat', str_origin, str_destination + '/data')
    # creazione dir timeseries_shift
    check_path_and_clean(str_destination + '/timeseries_shift')
    file_copy('timeseries-100-k-24-h-shift.dat', str_origin, str_destination + '/timeseries_shift')

    # creazione dir logs e matlab
    check_path_and_clean(str_destination + '/logs')
    check_path_and_clean(str_destination + '/matlab')

# debug
# copyFile('poa.csv',strOrigin,strDestination+'/matlab')
# copyFile('iwc.csv',strOrigin,strDestination+'/matlab')
# copyFile('iterations.csv',strOrigin,strDestination+'/matlab')
# copyFile('time.txt',strOrigin,strDestination+'/matlab')
# copyFile('violations.txt',strOrigin,strDestination+'/logs')
# copyFile('potential.csv',strOrigin,strDestination+'/matlab')
# copyFile('workloads.csv',strOrigin,strDestination+'/matlab')
# copyFile('cost.csv',strOrigin,strDestination+'/matlab')
