from pandas import read_excel
from datetime import datetime
from django.core.management.base import BaseCommand
from hla.models import Results, Patients, Tests, Locus

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self)
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Deleting Result & Test instances")
    Results.objects.all().delete()
    Tests.objects.all().delete()


def run_seed(self):
    # Step 0: delete tables?
    clear_data()

    # Step 1: Insert file to be converted and Date of Test (in HLA_DB directory)
    filename = "19NGS44 Set A export.xlsx"
    date_of_test = "Oct 8 2019 15:45:25"

    # Step 2: Initialise data structures
    patientsDict = {}

    # Step 3: Do converting
    df = read_excel(filename, sheet_name="Transfer set A & B")
    dateOfTest = datetime.strptime(date_of_test, '%b %d %Y %H:%M:%S')
    # create test instance in Tests table
    Tests.objects.create(testDate=dateOfTest)
    previousLocus = ""
    previousResult = ""
    for row in df.itertuples():
        print(row)
        # create patient instance in Patients table (if patient is already in DB then gets ID)
        patient = str(row.Name)
        print("Patient: " + patient)
        Patients.objects.get_or_create(patientNumber=patient)

        # create locus instance in Locus table (what happens if already there though??)
        locus = row.Component.split("*")[0]
        # handle DBR3/4/5 combo
        if locus == "HLA-DRB3/4/5" and row.Result != "X":
            locus = "HLA-DRB" + row.Result.split("*")[0]
            previousLocus = locus
        if locus == "HLA-DRB3/4/5" and row.Result == "X":
            locus = previousLocus
        print("Locus: " + locus)
        # object creation is unneccessary if locus migration worked
        #Locus.objects.create(locusName=locus)

        # get result
        result = row.Result
        print("Result (before 3/4/5) : " + result)
        # handle DBR3/4/5
        if (locus == "HLA-DRB3" or locus == "HLA-DRB4" or locus == "HLA-DRB5") and result != "X":
            print("handling locus")
            result = row.Result.split("*")[1]
        print("Result (after 3/4/5): " + result)

        # handle "X" on second copy (meaning homozygote)
        copy = row.Component.split("*")[1]
        print("Copy: " + copy)
        if copy == "1":
            previousResult = result
        if copy == "2" and row.Result == "X":
            result = previousResult
            print("Result changed from X to " + result)

        # save result in Results table (& link to other tables)
        #Results.objects.create(result=result)
        print("Getting locus ID")
        locus_id = Locus.objects.get(locusName=locus)
        print("Getting patient ID")
        patient_id = Patients.objects.get(patientNumber=patient)
        print("Getting test ID")
        test_id = Tests.objects.get(testDate=dateOfTest)
        print("Making results object")
        Results.objects.create(result=result,
                                patientID=patient_id,
                                testID=test_id,
                                locusID=locus_id)
        #resultsTable = Results(My_code='some code', Location='India', status_ID=status)
        #resultsTable.save()
        

    # Step 4: Profit??
