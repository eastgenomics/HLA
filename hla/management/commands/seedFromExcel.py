from django.core.management.base import BaseCommand
from pandas import read_excel
from datetime import datetime
from hla.models import Results, Patients, Tests, Locus
from django.db import IntegrityError
import collections


class Command(BaseCommand):
    help = "Seed database for testing and development. NB - deletes DB first."

    def add_arguments(self, parser):
        parser.add_argument('input', type=str, help="Input excel")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        if run_seed(options['input']) > 0:
            self.stdout.write('seeding failed.')
        else:
            self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Deleting Result & Test instances")
    Results.objects.all().delete()
    Tests.objects.all().delete()


def checkConfirmed(result_object):
    # filter results table by patientID and locusID
    results_list = Results.objects.filter(patientID=result_object.patientID,
                                          locusID=result_object.locusID)
    # get results as dict (testDate as key)
    test_dict = collections.defaultdict(list)
    for res in results_list:
        test_dict[res.testID].append(res.result)
    # if this gives more than 1 entry (i.e. not just itself) confirmed = true
    if len(results_list) > 1:
        return (True, results_list)
    else:
        return (False, results_list)


def importData(excel_file):
    print("Importing data into database")
    # Get test results into dataframe (& check if valid)
    try:
        df = read_excel(excel_file, sheet_name="Transfer set A & B")
    except Exception:
        print("Input file not recognised. Is it the NGS excel export?")
        return 1

    # Get datetime of test (test identifier)
    date_df = read_excel(excel_file, sheet_name='Summary', header=None)
    date_raw = date_df.loc[1, 1]
    dateOfTest = datetime.strptime(date_raw, '%b %d %Y %H:%M:%S')

    # create test instance in Tests table (& catch duplicates)
    try:
        Tests.objects.create(testDate=dateOfTest)
    except IntegrityError:
        print("There is already a test with this datetime in the DB.")
        return 1

    # initialise variables for remembering previous alleles (handles X)
    previousLocus = ""
    previousResult = ""

    # iterate through dataframe
    for row in df.itertuples():
        # create patient instance in Patients table (or just gets ID if exists)
        patient = str(row.Name)
        Patients.objects.get_or_create(patientNumber=patient)

        # create locus instance in Locus table
        locus = row.Component.split("*")[0]
        # handle DBR3/4/5 combo
        if locus == "HLA-DRB3/4/5" and row.Result != "X":
            locus = "HLA-DRB" + row.Result.split("*")[0]
            previousLocus = locus
        if locus == "HLA-DRB3/4/5" and row.Result == "X":
            locus = previousLocus
        # object creation is unneccessary if locus migration worked

        # get result
        result = row.Result
        # handle DBR3/4/5
        if (locus == "HLA-DRB3" or locus == "HLA-DRB4"
                or locus == "HLA-DRB5") and result != "X":
            result = row.Result.split("*")[1]

        # handle "X" on second copy (meaning homozygote)
        copy = row.Component.split("*")[1]
        if copy == "1":
            previousResult = result
        if copy == "2" and row.Result == "X":
            result = previousResult

        # save result in Results table (& link to other tables)
        locus_id = Locus.objects.get(locusName=locus)
        patient_id = Patients.objects.get(patientNumber=patient)
        test_id = Tests.objects.get(testDate=dateOfTest)
        new_obj = Results.objects.create(result=result, patientID=patient_id,
                                         testID=test_id, locusID=locus_id)
        
        # check whether this confirms previous results & update previous
        # entries to confirmed if neccessary
        conf = checkConfirmed(new_obj)
        if conf[0]:
            new_obj.confirmed = True
            for prev_res in conf[1]:
                prev_res.confirmed = True
                prev_res.save()
        else:
            new_obj.confirmed = False
        new_obj.save()
    return 0


def run_seed(inp):
    # Delete whatever crap is already there
    clear_data()

    # Import new data from excel
    if importData(inp) > 0:
        return 1
    else:
        return 0
