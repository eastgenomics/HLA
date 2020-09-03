from django.db import models
from django.utils import timezone
from django.core import validators
from datetime import date


CONFIRMED_CHOICES = [
    ('y', 'Yes'),
    ('n', 'No'),
]


class Patients(models.Model):
    patientNumber = models.CharField(max_length=15, unique=True, default=None)
    patientID = models.AutoField(primary_key=True)


class Locus(models.Model):
    locusID = models.AutoField(primary_key=True)
    locusName = models.CharField(max_length=30)

class Tests(models.Model):
    testID = models.AutoField(primary_key=True)
    testDate = models.DateField(auto_now=False, default=date.today)
    confirmed = models.CharField(max_length=1, choices=CONFIRMED_CHOICES)


class Results(models.Model):
    patientID = models.ForeignKey(Patients, on_delete=models.CASCADE)
    resultID = models.AutoField(primary_key=True)
    testID = models.ForeignKey(Tests, on_delete=models.CASCADE)
    locusID = models.ForeignKey(Locus, on_delete=models.CASCADE)
    result = models.CharField(max_length=20)











class ImportData(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"