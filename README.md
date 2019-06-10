# INSTALLATION

## METHOD 1: ONLY WITH PIP AND VIRTUALENV
Installation of the Python environment with pip and virtualenv

### 1 Check python version
Check version
```bash
python --version
OUTPUT: Python 3.7.3
```

python3
=> Command should be available

### 2 Install pip
```bash
apt-get install pip
```

### 3 Install virtual env
```bash
pip install virtualenv
```

### 4 Create a virtual env in the project directory for the project

It creates a virtual environment only for the project. As a consequence it creates a directory in the project with all binary files for python / modules ...

Execute:
```bash
virtualenv -p python3 backuppip
```

### 5 Activate the virtual env
```bash
source backuppip/bin/activate
```

### 6 Add module to the virtual env
```bash
pip install python-osc
pip install pandas
```

##METHOD 2: MICROCONDAS (Mac)
Installation of the Python environment with minicondas

### 1 Install minicondas
#### 1) Execute ssh file
https://conda.io/en/latest/miniconda.html

Execution:
```bash
chmod u+x Miniconda3-latest-MacOSX-x86_64.sh
./Miniconda3-latest-MacOSX-x86_64.sh
```

Miniconda3 will now be installed into this location:
/Users/XXXXXXX/miniconda3

#### 2) Install is finish here (output)
installing: conda-4.6.14-py37_0 ...
installation finished.
Do you wish the installer to initialize Miniconda3
by running conda init? [yes|no]
[yes] >>> yes
no change     /Users/XXXXXXX/miniconda3/condabin/conda
no change     /Users/XXXXXXX/miniconda3/bin/conda
no change     /Users/XXXXXXX/miniconda3/bin/conda-env
no change     /Users/XXXXXXX/miniconda3/bin/activate
no change     /Users/XXXXXXX/miniconda3/bin/deactivate
no change     /Users/XXXXXXX/miniconda3/etc/profile.d/conda.sh
no change     /Users/XXXXXXX/miniconda3/etc/fish/conf.d/conda.fish
no change     /Users/XXXXXXX/miniconda3/shell/condabin/Conda.psm1
no change     /Users/XXXXXXX/miniconda3/shell/condabin/conda-hook.ps1
no change     /Users/XXXXXXX/miniconda3/lib/python3.7/site-packages/xonsh/conda.xsh
no change     /Users/XXXXXXX/miniconda3/etc/profile.d/conda.csh
modified      /Users/XXXXXXX/.bash_profile

#### 3) Check version
/Users/XXXXXXX/miniconda3/bin/python3 --version
OUTPUT: Python 3.7.3

#### 4) Install the env
Execution example (use a python version of miniconda)
/Users/XXXXXXX/miniconda3/bin/python3 /Users/XXXXXXX/... project/project.py

##### a) Install condas
/Users/XXXXXXX/miniconda3/bin/conda install

### 2 Create a specific environment with pandas
/Users/XXXXXXX/miniconda3/bin/conda create --name backuppj pandas

IT CREATE AN ENVIRONEMENT DIRECTLY WITH PANDAS

### 3 Activate this new environment
You need to know which shell you have (here bash)

Note: How to know your bash version:
```bash
echo $0
```
-bash

Init. environement:
/Users/XXXXXXX/miniconda3/bin/conda init bash
/Users/XXXXXXX/miniconda3/bin/conda activate backuppj

Or direcly
```bash
conda activate backuppj
```

Note: You need to restart your shell at that moment

### 4 Create a pip virtual environment

#### a) Create a virtual env
```bash
pip install virtualenv
virtualenv backuppip
```

==> it creates a dir and files

#### b) Activate the virtual env
```bash
source backuppip/bin/activate
```

#### c) NOW THE CONDAS ENV IS ON PYTHON "3" BIN ENV AND ANY NEW MODULES ARE INSTALL IN THE VIRTUAL ENV

Note 1: Desactivate the pip env:
deactivate

Note 2: Python version used
Only with condas
$ which python
/Users/XXXXXXXX/miniconda3/envs/backuppj/bin/python
After pip activation:
$ which python
/Users/XXXXXXX/Documents/...projectDirectory.../backup/backuppip/bin/python

### 5 Add module to this new virtual environment
a) Add OSC module:
```bash
pip install python-osc
```

Output:
Successfully installed python-osc-1.7.0

Not used (python-osc is not available):
conda install --name backuppj -c attwad python-osc
conda install --name backuppj -c auto python-osc


# HOW TO USE IT

## 1 Go in the directory of your program
```bash
cd .../backup
```

## 2 Be sure that your PIP virtualenv is started:
```bash
source backuppip/bin/activate
```

## 3 Start the program who sends OSC mode 

```bash
python send_osc_mode.py
```

This program tells the user to set a mode (1 or 2 or 3 or ... or 'exit')

It will send on the network an OSC message to the other program in order to select a 

## 4 Start the program who receives an OSC mode in order to return a selection of physical objects.
Thos objects are listed in a limited number of columns and it sends another OSC message with the list of object id in a string.

```bash
python select_objects_with_osc_mode.py
```