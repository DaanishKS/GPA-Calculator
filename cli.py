import os
import sys
import yaml

from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

from transcript import Transcript


def file_completion():
    files = []
    for f in os.listdir('./'):
        file_name, file_extension = os.path.splitext(f)
        if file_extension in {'.csv', '.CSV'}:
            files.append(f)
    return WordCompleter(files)


def file_validation():
    files = []
    for f in os.listdir('./'):
        file_name, file_extension = os.path.splitext(f)
        if file_extension in {'.csv', '.CSV'}:
            files.append(f)
    is_valid = lambda text: text in files
    return Validator.from_callable(
        is_valid,
        error_message=
        'Please enter the name of a CSV file in the working directory.')


def yes_no_validation():
    is_valid = lambda text: text in [
        'Y', 'y', 'YES', 'Yes', 'yes', 'N', 'n', 'NO', 'No', 'no'
    ]
    return Validator.from_callable(
        is_valid, error_message='Please enter "y" or "n" only.')


def report_type_validation():
    is_valid = lambda text: text in ['1', '2']
    return Validator.from_callable(
        is_valid, error_message='Please enter "1" or "2" only.')


def cli():
    print(f'###########################\n'
           '#   GPA Calculator v0.3   #\n'
           '# Developed by Daanish KS #\n'
           '###########################\n')

    session = PromptSession()  # Enables file path history for convenience

    while True:
        csv_file = session.prompt('Transcript CSV file path: ',
                                  completer=file_completion(),
                                  validator=file_validation(),
                                  validate_while_typing=True)
        x = Transcript(csv_file)

        file_request = prompt('Write GPA report to file [y/n]? ',
                              validator=yes_no_validation(),
                              validate_while_typing=True)

        if file_request in {'Y', 'y', 'YES', 'Yes', 'yes'}:
            report_type = prompt('JSON [1] or YAML [2]? ',
                                 validator=report_type_validation(),
                                 validate_while_typing=True)
            if report_type == '1':
                x.gpa_report_to_file(file_path='gpa_report.json')
            if report_type == '2':
                x.gpa_report_to_file(file_path='gpa_report.yaml')
        print()
        yaml.dump(x.gpa_report(round_place=3), sys.stdout)
        print()

        repeat_request = prompt('Continue [y/n]? ',
                                validator=yes_no_validation(),
                                validate_while_typing=True)
        if repeat_request in {'N', 'n', 'NO', 'No', 'no'}:
            break
        else:
            print(f'\n-------------------------\n')


if __name__ == "__main__":
    cli()
