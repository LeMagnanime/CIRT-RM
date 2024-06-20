from django.forms import ModelForm
from django import forms
from .models import *

#formulaire pour l'ajout des actifs
class AssetForm(ModelForm):
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
