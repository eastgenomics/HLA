from pandas import read_excel
from datetime import datetime
from hla.models import Results, Patients, Tests, Locus

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
previousAllele = ""
for row in df.itertuples():
    # create patient instance in Patients table (what happens if already there though??)
    patient = row.Name
    print(patient)
    Patients.objects.create(patientNumber=patient)

    # create locus instance in Locus table (what happens if already there though??)
    locus = row.Component.split("*")[0]
    # handle DBR3/4/5 combo
    if locus == "HLA-DRB3/4/5" and row.Result != "X":
        locus = "HLA-DRB" + row.Result.split("*")[0]
    Locus.objects.create(locusName=locus)

    # get result
    result = row.Result
    # handle DBR3/4/5
    if [locus == "HLA-DRB3" or locus == "HLA-DRB4" or locus == "HLA-DRB5"] and row.Result != "X":
        result = row.Result.split("*")[1]

    # handle "X" on second copy (meaning homozygote)
    copy = row.Component.split("*")[1]
    if copy == "1":
        previousAllele = result
    if copy == "2" and row.Result == "X":
        result = previousAllele

    # save result in Results table (& link to other tables)
    Results.objects.create(result=result)
    locus_id = Locus.objects.get(locusName=locus)
    patient_id = Patients.objects.get(patientNumber=patient)
    test_id = Tests.objects.get(testDate=date_of_test)
    Results.objects.create(result=result,
                            patientID=patient_id,
                            testID=test_id,
                            locusID=locus_id)
    #resultsTable = Results(My_code='some code', Location='India', status_ID=status)
    #resultsTable.save()
    

# Step 4: Profit??
