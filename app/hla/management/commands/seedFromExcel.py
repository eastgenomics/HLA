from django.core.management.base import BaseCommand
from pandas import read_excel, ExcelFile
from datetime import datetime
from hla.models import Results, Patients, Tests, Locus
from django.db import IntegrityError
import re


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


def calculateAlleleFrequency(result_object):
    """
    Takes an object from the Results table & calculates how often that allele
    appears in the DB. WARNING - does not account for DRB3/4/5!
    """
    geneNum = len(Results.objects.filter(locusID=result_object.locusID))
    alleleNum = len(Results.objects.filter(locusID=result_object.locusID,
                                           result=result_object.result))
    AF = alleleNum / geneNum
    return round(AF, 7)


def constructURL(result_object):
    """
    Takes a result object (from results table) & constructs a URL that should
    link to the EBI HLA DB entry for the relevant allele. If there are multiple
    results (ambiguous call) then multiple URLs are returned.
    """
    allele_list = []
    if result_object.locusID.locusName == "HLA-DRB3/4/5":
        locus = result_object.result.split("*")[0]
        for res in result_object.result.split("*")[1].split("/"):
            allele_string = "DRB" + locus + "*" + res
            allele_list.append(allele_string)
    else:
        for res in result_object.result.split("/"):
            allele_string = (result_object.locusID.locusName.split("-")[1]
                             + "*" + res)
            allele_list.append(allele_string)
    urls_list = ""
    for a_str in allele_list:
        ebi_url = ("https://www.ebi.ac.uk/cgi-bin/ipd/imgt/hla/get_allele.cgi?"
                   + a_str)
        urls_list = urls_list + " " + ebi_url
    return urls_list


def importData(excel_file):
    print("Importing data into database...")
    # Get test results into dataframe (& check if valid)
    try:
        inp = ExcelFile(excel_file)
        sheets = inp.sheet_names
        df = read_excel(excel_file, sheet_name=-1)
    except Exception:
        print("Input file not recognised. Is it the NGS excel export?")
        return 1

    # Get datetime of test (test identifier)
    date_df = read_excel(excel_file, sheet_name='Summary', header=None)
    date_raw = date_df.loc[1, 1]
    dateOfTest = datetime.strptime(date_raw, '%b %d %Y %H:%M:%S')
    run_id = str(excel_file).split(' ')[0]

    # create test instance in Tests table (& catch duplicates)
    try:
        Tests.objects.create(testDate=dateOfTest, testRunID=run_id)
    except IntegrityError:
        print("There is already a test with this datetime or RunID in the DB.")
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
            if result == "X":
                continue
        if copy == "2" and row.Result == "X":
            if previousResult == "X":
                continue
            result = previousResult

        # save result in Results table (& link to other tables)
        locus_id = Locus.objects.get(locusName=locus)
        patient_id = Patients.objects.get(patientNumber=patient)
        test_id = Tests.objects.get(testDate=dateOfTest)
        new_obj = Results.objects.create(result=result, patientID=patient_id,
                                         testID=test_id, locusID=locus_id)

        # calculate allele frequency & update previous entries
        AF = str(calculateAlleleFrequency(new_obj))
        obj_list = Results.objects.filter(result=new_obj.result,
                                          locusID=new_obj.locusID)
        for obj in obj_list:
            obj.alleleFreq = AF
            obj.save()

        # get URLs for EBI DB entries to link to
        urls = constructURL(new_obj)
        new_obj.externalInfo = urls
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
