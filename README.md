# GTExperimentLauncher

A bunch of python scripts to launch experiments for GT paper.

### Dependencies

GTExperimentLauncher has been tested with Python 2.7 and it
requires the installation of the following external packages:
* **paramiko** (for ssh connection)
* **numpy** (for mathematical calculations)

### Hands on

To execute the launcher
execute `python GTLauncher.py`. A multiple-choice menu will
appear. From there the user can decide to execute the various phases of the
experiments one by one or all together. In particular, the menu permits to:
1. Check the correctness of the `properties.ini` file, which contains the
information required to run the exeriments (connection settings, folders, parameters)
2. Clean the remote folder
3. Upload the experiment folder to the server
4. Launch the experiments in parallel the UNIX `screen` command is used to
launch in parallel several algorithms. When all the experiments are done results are gathered
and indexes are calculated
5. Compress the results and download them in a folder previously defined by the user

### properties.ini

This is an example of the properties.ini file used to configure the experiments.
The program helps the user to generate it in the correct way, tough.
```
**[connection settings]**

ip_server = server.domain

username = my_username

password = XXX

**[general settings]**

remote_path = /home/XXX

algo_list = alg2_1, alg2_2

phi_list = 0.3

num_repetitions = 1

max_ni = 100

min_ni = 80

increasing_step = 5

folder_name = GTExperimentLauncher

experiment_name = Exp_name

download_folder = /home/XXX
```



The first stable version has been released on 05.07.2016.

