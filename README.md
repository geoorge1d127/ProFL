# ProFL: A Fault Localization Tool for Prolog


ProFL is a command-line fault localization tool for Prolog models. Given a faulty Prolog model and a corresponding test suite, ProFL will calculate which Prolog statements are the most likely to be faulty or have the highest "suspiciousness". ProFL has three components: A tool that determines test coverage for the given test suite on the Prolog model, ProFL-s which is a spectrum-based fault localization technique and ProFL-m which is a mutation-based fault localization technique.


# Motivation
In the field of software testing, there seems to be useful tools and techniques when it comes to localizing faults in imperative languages (Java and C++). However, there seems to be a lack of research as to how these techniques might be useful for declarative languages, like Prolog. Since Prolog is still widely used, this project aims to address the need to enable afault localization in Prolog models.


# Requirements:


* Operating systems:
  - Linux (64 bit)
  - Mac OS (64 bit)


* Dependencies
  - Python(2.7 or Above): Must be installed and accessible from `PATH`.
  - Python library PrettyTable: Must be installed using pip.
  - Python libray Click: Must be installed using pip
  - Swipl(Swi-Prolog command line tool): Must be installed and accessible from `PATH`


# Installation

## Install Python
[Python](https://www.python.org/downloads/) - Install python 2.7 or Above

## Install Swi-Prolog
[Swi-Prolog](https://www.swi-prolog.org/download/stable) - Install Stable Version

## Install Python Depencies
[PrettyTable](https://pypi.org/project/PrettyTable/)
To install PrettyTable using pip, Open a terminal and run:
```Shell
pip install PrettyTable
```
[Click](https://pypi.org/project/click/)
To install CLick Using pip, Open a terminal and run:
```Shell
pip install click
```

# Getting Started:

## Clone ProFL repo

To run `ProFL`, use `git` to clone the repository.

```Shell
git clone https://github.com/geoorge1d127/ProFL.git
```

## Calculate Suspiciousness

To calculate the suspiciousness of a faulty Prolog model, run
```Shell
python ProFL.py -p <arg> -t <arg> -f <arg> -v <arg> [-s <arg>] [-r <arg>] [-c <arg>]

```
or use the full argument name
```Shell
python ProFL.py --program-path <arg> --test-suite <arg> --fl-technique <arg> --view <arg> [--suspicious-formula <arg>] [--result-path <arg>] [--coverage-path <arg>]
```



* `-p,--program-path`: This argument isrequired. Pass the filename of the faulty Prolog program.

* `-t,--test-suite`: This argument is required. Pass the file name of the plunit test suite.

* `-f,--fl-technique`: This argument is required. Pass the fault localization technique to use. The value should be `-spectrum`,`-mutation`, or `-both`.

* `-v,--view`: This argument is required. Pass how much of the ranked  suspicious  list  to  view.  The  value  should  be  `-top1`,`-top5`, `-top10`, or `-all`.

* `-s,--suspicious-formula`: This argument is optional and is used when the fault localization technique is `-spectrum` or`-both`. Pass the suspiciousness formula for ProFLs to use. The value should be `-tarantula`, `-ochiai`, or `-op2`.If specifying more than one, separate with a comma, i.e. `-ochiai, -op2`. If not specified, all three are used.

* `-r,--result-path`: This argument is optional. Pass the path to which you want to save the fault localization results. If not specified, the results are only printed to the terminal.

* `-c,--coverage-path`: This argument is optional. Pass the path to which you want to save the coverage results calculated during ProFL. If not specified, the coverage information is not saved.

For each run, the command reports up to four tables (depending on which technique and suspiciousness formulas you choose) ranking potentially faulty statements by their suspiciousness score. The tables will show either: The most suspicious statement, the top 5 most suspicious statement, the top 10 most suspicious statement, or all of the statements in order of most suspicious to least suspicious. You also have the option of printing out the results as an html webpage.

# Components
