from gpa_calculator import Transcript
import sys

if __name__ == "__main__":
    # Read in the transcript CSV file name as a command line argument.
    x = Transcript(sys.argv[1])

    # Calculate overall university GPA and output a GPA report YAML file.
    periods = []
    print(x.calculate_gpa(periods,3,'University','Overall'))
    x.gpa_report(periods, 3, 'gpa_report.yaml')
