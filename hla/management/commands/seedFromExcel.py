from django.core.management.base import BaseCommand
from pandas import read_excel
from datetime import datetime
from hla.models import Results, Patients, Tests, Locus
from django.db import IntegrityError
import collections
import itertools


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
    """
    Checks whether a result confirms any previous result already in the DB.
    Returns True or False, plus any confirmed previous results.
    """
    # filter results table by patientID and locusID
    results_list = Results.objects.filter(patientID=result_object.patientID,
                                          locusID=result_object.locusID)
    # get results & indices as dict (grouping by testDate as key)
    test_dict = collections.defaultdict(list)
    for res in results_list:
        test_dict[res.testID].append((res.result, res.resultID))
    # convert to list of results grouped by test (sort to aid comparison later)
    sorted_vals = []
    for v in test_dict.values():
        sorted_vals.append(sorted(v))
    # abort & return False if there's an odd number of results (this means the
    # second allele is not in the DB yet so will foul the rest of the function)
    if len(set(itertools.chain.from_iterable(sorted_vals))) % 2 == 1:
        return (False, set())
    # swap values around (as we only want to compare the results, not indices)
    swaplist = []
    for val in sorted_vals:
        result_tuple = (val[0][0], val[1][0])
        index_tuple = (val[0][1], val[1][1])
        swaplist.append((result_tuple, index_tuple))
    # do pairwise comparison of results (avoiding self-comparisons)
    comp = [(x[0] == y[0], x[1], y[1]) for i, x in enumerate(swaplist)
            for j, y in enumerate(swaplist) if i != j]
    # get list of previous results that are confirmed by result_object
    change_ids = []
    for i in comp:
        if i[0]:
            change_ids.append(i[1])
            change_ids.append(i[2])
    # return True if any pairwise comparison was True,
    # and the unique set of confirmed result IDs
    return (any(comp), set(itertools.chain.from_iterable(change_ids)))


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
    # previousLocus = ""
    previousResult = ""

    # iterate through dataframe
    for row in df.itertuples():
        # create patient instance in Patients table (or just gets ID if exists)
        patient = str(row.Name)
        Patients.objects.get_or_create(patientNumber=patient)

        # create locus instance in Locus table
        locus = row.Component.split("*")[0]
        # handle DBR3/4/5 combo - temporarily removed while I think about this
        '''
        if locus == "HLA-DRB3/4/5" and row.Result != "X":
            locus = "HLA-DRB" + row.Result.split("*")[0]
            previousLocus = locus
        if locus == "HLA-DRB3/4/5" and row.Result == "X":
            locus = previousLocus
        '''
        # object creation is unneccessary if locus migration worked

        # get result
        result = row.Result
        # handle DBR3/4/5 - as above
        '''
        if (locus == "HLA-DRB3" or locus == "HLA-DRB4"
                or locus == "HLA-DRB5") and result != "X":
            result = row.Result.split("*")[1]
        '''

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
            for idx in conf[1]:
                prev_res = Results.objects.get(resultID=idx)
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
