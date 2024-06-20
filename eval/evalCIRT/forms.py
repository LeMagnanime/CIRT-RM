from django import forms
from .models import Company
from django.forms import ModelForm
from .models import Document
from .models import Donnee

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'number', 'address', 'email', 'date']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'file']

class DonneeForm(forms.ModelForm):
    class Meta:
        model = Donnee
        fields = ['maturite', 'risque', 'Reponse', 'id_risque', 'occurence', 'gravite', 'detection', 'criticite', 'recommandation', 'risque_brute', 'responsable']