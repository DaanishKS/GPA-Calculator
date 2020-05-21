# gpa-calculator

A GPA calculator primarily intended for use for US medical school application
services such as AMCAS and TMDSAS. The program, written in Python, computes
various types of GPAs.

A simple demo that makes use of the `Transcript` class has been provided as
`demo.py`. Given a transcript CSV file `transcript.csv`, the overall university
GPA can be calculated by navigating to the working directory and executing the
script (along with a single command line argument---the CSV file name):

```console
$ python demo.py transcript_template.csv
{'GPA Point Sum': 38.68, 'Credit Hours': 10, 'GPA': 3.868}
"gpa_report.yaml" created/updated.
```
