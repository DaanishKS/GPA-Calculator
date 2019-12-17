import pandas as pd
import sys
import yaml


def gpa_calculator(file):

    university_grade_key = {
        'A+': 4.00,
        'A': 4.00,
        'A-': 3.67,
        'B+': 3.33,
        'B': 3.00,
        'B-': 2.67,
        'C+': 2.33,
        'C': 2.00,
        'C-': 1.67,
        'D+': 1.33,
        'D': 1.00,
        'D-': 0.67,
        'F': 0.00
    }

    aamc_grade_key = {
        'A+': 4.0,
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'D-': 0.7,
        'F': 0.0
    }

    tmdsas_grade_key = {
        'A+': 4.0,
        'A': 4.0,
        'A-': 4.0,
        'B+': 3.0,
        'B': 3.0,
        'B-': 3.0,
        'C+': 2.0,
        'C': 2.0,
        'C-': 2.0,
        'D+': 1.0,
        'D': 1.0,
        'D-': 1.0,
        'F': 0.0
    }

    gpa_data = {
        'School': {
            'Total': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            },
            'BCPM': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            },
            'AO': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            }
        },
        'AMCAS': {
            'Total': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            },
            'BCPM': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            },
            'AO': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            }
        },
        'TMDSAS': {
            'Total': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            },
            'BCPM': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            },
            'AO': {
                'GPA Points': 0,
                'Credits': 0,
                'GPA': 0
            }
        }
    }

    gpa_data['School']['Grade Key'] = university_grade_key
    gpa_data['AMCAS']['Grade Key'] = aamc_grade_key
    gpa_data['TMDSAS']['Grade Key'] = tmdsas_grade_key

    df = pd.read_csv(file)

    transcript = df[['Credit Hours', 'Grade', 'Type']].values.tolist()

    for credit_hours, grade, class_type in transcript:
        for i, j in gpa_data.items():
            j['Total']['GPA Points'] += credit_hours * j['Grade Key'][grade]
            j['Total']['Credits'] += credit_hours

            if class_type == 'BCPM':
                j['BCPM']['GPA Points'] += credit_hours * j['Grade Key'][grade]
                j['BCPM']['Credits'] += credit_hours

            elif class_type == 'AO':
                j['AO']['GPA Points'] += credit_hours * j['Grade Key'][grade]
                j['AO']['Credits'] += credit_hours

    for i, j in gpa_data.items():
        j.pop('Grade Key')
        for k, v in j.items():
            v['GPA'] = round(v['GPA Points'] / v['Credits'], 3)
            v['GPA Points'] = round(v['GPA Points'], 3)
            print(f'{i} {k} GPA: {v["GPA"]}')
        print()

    with open('GPA Report.yml', 'w') as file:
        yaml.dump(gpa_data, file)

    return gpa_data


if __name__ == "__main__":
    gpa_calculator(sys.argv[1])