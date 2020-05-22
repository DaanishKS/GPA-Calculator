import pandas as pd
import numpy as np
import json
import yaml
import os


class Transcript:
    """
    The Transcript class holds data related to an actual university
    transcript and performs GPA calculation operations.

    In short, there are three GPA scales that can be used to translate
    letter grades to GPA points: the University scale, AMCAS scale, and
    TMDSAS scale. The latter two are utilized in the calculation of GPA
    for medical school admissions.

    Furthermore, there are three "types" of GPAs that can be calculated
    from a transcript: Overall; Biology, Chemistry, Physics, Math
    (BCPM); and All Other (AO). Again, the latter two are primarily
    considered for medical school admissions.

    Thus, there are nine possible GPA permutations of GPA scale and type.

    Parameters
    ----------
    csv_file : str
        This is the name of the CSV file from where we are obtaining our
        transcript data.

    Attributes
    ----------
    data : pandas.DataFrame
        This is the internal representation of the data obtained from
        the original CSV file. The usage of Pandas allows for efficient
        value manipulation and calculation.
    gpa_scales : list of str
        This is a list of all acceptable GPA scales that are eligible for
        calculation. These scales translate course letter grades to GPA
        points.
    gpa_types : list of str
        This is a list of all acceptable GPA types that are eligible for
        calculation. These types dictate which courses will be considered
        when calculating a GPA.
    """

    def __init__(self, csv_file):
        with open('gpa_scales.json', 'r') as f:
            gpa_scales = json.load(f)

        df = pd.read_csv(csv_file)
        for col in list(df.columns):
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()

        # Calculate various GPA points for each course.
        for scale in gpa_scales:
            gpa_points = [
                gpa_scales[scale][row.Grade] * row.Credit_Hours
                for row in df.itertuples()
            ]
            df[f'{scale}_GPA_Points'] = np.asarray(gpa_points)

        self.data = df
        self.gpa_scales = ['University', 'AMCAS', 'TMDSAS']
        self.gpa_types = ['Overall', 'BCPM', 'AO']

    def calculate_gpa(self, gpa_scale, gpa_type,
                      periods=None, round_place=None):
        """
        Calculates cumulative GPAs, or over a given set of grading periods.

        Parameters
        ----------
        gpa_scale : {'University', 'AMCAS', 'TMDSAS'}, default 'University'
            Determines which GPA scale will be used when calculating
            cumulative GPA.
        gpa_type : {'Overall', 'BCPM', 'A0'}, default 'Overall'
            Determines what type of cumulative GPA will be calculated.
        periods : list of tuples of int, str; default None
            If provided, determines the grading periods (i.e., semesters)
            over which GPA should be calculated.
            Ex. [(2018, 'Fall'), (2019, 'Spring')]
        round_place: int, default None
            If provided, will round the output to the specified number of
            places after the decimal.

        Returns
        -------
        result : dict
            The resultant cumulative GPA.

        Raises
        ------
        ValueError
            If parameters gpa_scale or gpa_type do not equal an acceptable
            value.
        """
        if gpa_scale not in self.gpa_scales:
            raise ValueError('gpa_scale is not valid.')
        if gpa_type not in self.gpa_types:
            raise ValueError('gpa_type is not valid}')

        df = self.data.copy()

        if periods:
            filtered_df = df[df['Year'] == periods[0][0]][df['Semester'] ==
                                                          periods[0][1]]
            if len(periods) > 1:
                del periods[0]
                for year, semester in periods:
                    filtered_df = filtered_df.append(
                        df[df['Year'] == year][df['Semester'] == semester])
            df = filtered_df.copy()

        # Drop courses that do not count toward GPA at all.
        df.drop(df[df['Grade'] == 'CR'].index, inplace=True)
        df.drop(df[df['Grade'] == 'NC'].index, inplace=True)

        # Only include courses that contribute to selected GPA type.
        if gpa_type == 'BCPM':
            df = df[df['Type'] == 'BCPM']
        elif gpa_type == 'AO':
            df = df[df['Type'] == 'AO']

        gpa_point_sum = np.sum(df[f'{gpa_scale}_GPA_Points'])
        credits_count = np.sum(df['Credit_Hours'])
        calculated_gpa = gpa_point_sum / credits_count

        result = {
            'GPA Point Sum': gpa_point_sum.item(),
            'Credit Hours': credits_count.item(),
            'GPA': calculated_gpa.item()
        }

        if round_place:
            result['GPA Point Sum'] = round(result['GPA Point Sum'],
                                            round_place)
            result['GPA'] = round(result['GPA'], round_place)

        return result

    def gpa_report(self, periods=None, round_place=None):
        """
        Calculates all possible GPA permutations.

        Parameters
        ----------
        periods : list of tuples of int, str; default None
            If provided, determines the grading periods (i.e., semesters)
            over which GPA should be calculated.
            Ex. [(2018, 'Fall'), (2019, 'Spring')]
        round_place: {int, None}, default 3
            If provided, will round the output to the specified number of
            places after the decimal.

        Returns
        -------
        report : dict
            The results of the GPA report.
        """
        # Initialize empty nested dict
        report = {n: {m: '' for m in self.gpa_types} for n in self.gpa_scales}

        # Populate dict
        for gpa_scale in report.keys():
            for gpa_type in report[gpa_scale].keys():
                report[gpa_scale][gpa_type] = self.calculate_gpa(
                    gpa_scale, gpa_type, periods, round_place)

        return report

    def gpa_report_to_file(self, file_path='gpa_report.yaml',
                              periods=None, round_place=3):
        """
        Outputs GPA report to either a JSON or YAML file.

        Parameters
        ----------
        file_path : str, default 'gpa_report.yaml'
            If provided, prints the computed GPA report as either a JSON
            or YAML.
        periods : list of tuples of int, str; default None
            If provided, determines the grading periods (i.e., semesters)
            over which GPA should be calculated.
            Ex. [(2018, 'Fall'), (2019, 'Spring')]
        round_place: int, default None
            If provided, will round the output to the specified number of
            places after the decimal.

        Raises
        ------
        ValueError
            If file path extension is not JSON or YAML.
        """
        report = self.gpa_report(round_place=round_place)

        file_name, file_extension = os.path.splitext(file_path)
        if file_extension == '.json':
            with open(file_path, 'w') as fp:
                json.dump(report, fp, indent=4)
            print(f'"{file_path}" created/updated.')
        elif (file_extension == '.yml') or (file_extension == '.yaml'):
            with open(file_path, 'w') as fp:
                yaml.dump(report, fp)
            print(f'"{file_path}" created/updated.')
        else:
            raise ValueError(
                '"{file_extension}" is not a valid file extension.')
