from django.db import models
from datetime import datetime


class Patients(models.Model):
    patientNumber = models.CharField(max_length=15, unique=True,
                                     default='unknown')
    patientID = models.AutoField(primary_key=True)


class Locus(models.Model):
    locusID = models.AutoField(primary_key=True)
    locusName = models.CharField(max_length=30)


class Tests(models.Model):
    testID = models.AutoField(primary_key=True)
    testDate = models.DateTimeField(auto_now=False, default=datetime.now,
                                    unique=True)


class Results(models.Model):
    patientID = models.ForeignKey(Patients, on_delete=models.CASCADE)
    resultID = models.AutoField(primary_key=True)
    testID = models.ForeignKey(Tests, on_delete=models.CASCADE)
    locusID = models.ForeignKey(Locus, on_delete=models.CASCADE)
    result = models.CharField(max_length=20)
    confirmed = models.BooleanField(default=False)
