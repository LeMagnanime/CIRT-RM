from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TypeActif)
admin.site.register(Asset)
admin.site.register(Menace)
admin.site.register(Vunlerabilite)
admin.site.register(EvaluationRisque)
admin.site.register(Domaine)