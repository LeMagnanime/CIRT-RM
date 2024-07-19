from django.forms import ModelForm
from django import forms
from .models import *

CRITICITE_CHOICES = [
    ('5', "5"),
    ('4', "4"),
    ('3', "3"),
    ('2', "2"),
    ('1', "1")
]

#formulaire pour l'ajout des actifs
class AssetForm(ModelForm):
    criticité = forms.ChoiceField(choices=CRITICITE_CHOICES, label="Criticité")
    class Meta:
        model = Asset
        fields = '__all__'

        widgets = {  
            'nom_actif' : forms.TextInput(attrs={'class':'form-control'}),
            'type_actif' : forms.Select(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'valeur_unitaire_actif' : forms.NumberInput(attrs={'class':'form-control'}),
            'cout_installation' : forms.NumberInput(attrs={'class':'form-control'}),
            'cout_entretien' : forms.NumberInput(attrs={'class':'form-control'}),
            'va' : forms.NumberInput(attrs={'class':'form-control'}),
            'valeur_indisponibilite' : forms.NumberInput(attrs={'class':'form-control'}),
            'criticité': forms.Select(attrs={'class': 'form-control'}),
        }

class AnalyseForm(ModelForm):
    class Meta:
        model = EvaluationRisque
        fields = ('actif', 'menaces', 'vulnerabilite', 'probabilite_occurrence', 'facteur_exposition')
           
        widgets = {  
            'actif' : forms.Select(attrs={'class':'form-control'}),
            'menaces' : forms.Select(attrs={'class':'form-control'}),
            'vulnerabilite': forms.Select(attrs={'class':'form-control'}),
            'probabilite_occurrence' : forms.NumberInput(attrs={'class':'form-control'}), 
            'facteur_exposition' : forms.NumberInput(attrs={'class':'form-control'}),
        }
