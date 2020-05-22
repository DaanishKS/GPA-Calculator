# GPA Calculator

This repository contains a Grade Point Average (GPA) calculator that is primarily intended for use for medical school application services such as AMCAS and TMDSAS. This calculator is written in Python and tooled as a CLI application. Various types of GPAs are calculated through the use of a defined `Transcript` class.

In order to use the CLI application, course and grade data (i.e. transcript) must be available in the working directory as a comma-separated values (CSV) file. This file, which can be edited using either a text editor or MS Excel, must have the following form (also provided in `transcript_template.csv`):

```csv
Year,Semester,Course,Credit_Hours,Grade,Type
2016,Fall,General Chemistry I,3,B,BCPM
2016,Fall,Introduction to Theater,3,A,AO
2016,Fall,MATH 2415,4,A-,BCPM
2017,Spring,CHEM 1312,3,A+,BCPM
```

As seen above, the `Course` column, which contains the name of the course, can be formatted however you prefer. The `Type` column refers to whether a course is either a "BCPM" course (Biology, Chemistry, Physics, Math) or "AO" (All Other). Every course in the CSV data file *must* be designated as one of these two types.

If you have Python 3 installed on your system, the most straightforward way to use the calculator is to first install `pipenv` and then execute the `cli.py` module as follows:

```console
$ pip install pipenv
$ pipenv run python cli.py
```

Alternatively, you can execute the `gpa_calculator.exe` file:

```console
$ .\gpa_calculator.exe
```

If you wish to build the executable file yourself, use the following sequence of commands (skip the first if you have `pipenv` already installed):

```console
$ pip install pipenv
$ pipenv shell
$ pipenv install
$ pyinstaller cli.py -F -n gpa_calculator --hidden-import="pkg_resources.py2_warn"
```
