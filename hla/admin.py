from django.contrib import admin
from hla.models import Results, Locus, Tests, Patients

# Register your models here.

admin.site.register(Results)
admin.site.register(Tests)
admin.site.register(Patients)
admin.site.register(Locus)
