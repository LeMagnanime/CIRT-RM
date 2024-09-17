from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class TypeActif(models.Model):
    class Meta:
        verbose_name = "Type d'actif"
        
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nom}"

class Asset(models.Model):
    class Meta:
        verbose_name = "Actif"
        
    CRITICITE_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ]
    
    type_actif = models.ForeignKey(TypeActif, on_delete=models.CASCADE)
    nom_actif = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    valeur_unitaire_actif = models.IntegerField()
    cout_installation = models.IntegerField()
    cout_entretien = models.IntegerField()
    va = models.IntegerField(editable=False)  # Empêche l'édition manuelle de ce champ dans l'admin
    valeur_indisponibilite = models.IntegerField()
    criticite = models.CharField(max_length=1, choices=CRITICITE_CHOICES)  # Nouveau champ pour la criticité

    def save(self, *args, **kwargs):
        # Calcul automatique de la valeur de l'actif
        self.va = self.valeur_unitaire_actif + self.cout_installation + self.cout_entretien
        super(Asset, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_actif}"

   
class Menace(models.Model):
    nom_menace = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    vulnerabilte = models.ManyToManyField('Vunlerabilite') 

    def __str__(self):
        return f"{self.nom_menace}"

class Domaine(models.Model):
    nom_domaine = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nom_domaine}"
    
class Vunlerabilite(models.Model):
    nom = models.CharField(max_length=200)
    code_cve = models.CharField(max_length=20)
    description = models.TextField()
    domaine = models.ForeignKey(Domaine, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.code_cve})"


class ActifMenace(models.Model):
    actif = models.ForeignKey(Asset, on_delete=models.CASCADE)
    menace = models.ForeignKey(Menace, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.actif} - {self.menace}"

def validate_probabilite(value):
    if not (1 <= value <= 5):
        raise ValidationError('La probabilité doit être comprise entre 1 et 5.',
            params={'value': value},
        )

class EvaluationRisque(models.Model):		 		
    actif = models.ForeignKey(Asset, on_delete=models.CASCADE)	
    menaces = models.ForeignKey(Menace, null=True, blank=True, on_delete=models.CASCADE)	
    vulnerabilite = models.ForeignKey(Vunlerabilite, on_delete=models.CASCADE) 
    id = models.AutoField(primary_key=True)
    risque = models.CharField(max_length=100, blank=True, editable=False)
    valeur_risque = models.IntegerField()
    facteur_exposition = models.FloatField()
    probabilite_occurrence = models.IntegerField(validators=[validate_probabilite]) #ou ARO(Annual rate of occurence)
    sle = models.FloatField(default=0) #facteur_expostion * valeur_actif
    impact_financier = models.FloatField(null=True, blank=True) 
    #impact_c = models.IntegerField(null=True, blank=True) 
    #impact_i = models.IntegerField(null=True, blank=True)
    #impact_d = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.actif}"

    def save(self, *args, **kwargs):
        self.facteur_exposition /= 100
        # Formatage de l'ID avec des zéros devant, par exemple 001, 002, etc.
        formatted_id = str(self.id).zfill(3)
        
        # Définir la valeur de risque
        self.risque = f"{self.actif.nom_actif}-R{formatted_id}"
        # Effectuer les calculs avant l'enregistrement
        self.sle = float(self.facteur_exposition) * self.actif.va # Assurez-vous que "valeur" est le champ approprié pour la valeur de l'actif
        self.impact_financier = int(self.sle * self.probabilite_occurrence)
        if self.impact_financier <= 10000:
            self.valeur_risque = 1
        elif 10000 < self.impact_financier <= 50000:
            self.valeur_risque = 2
        elif 50000 < self.impact_financier <= 200000:
            self.valeur_risque = 3
        elif 200000 < self.impact_financier <= 1000000:
            self.valeur_risque = 4
        else:  # impact_financier > 1000000
            self.valeur_risque = 5
        print(self.valeur_risque)

        # Appeler la méthode save() originale pour enregistrer l'objet
        super(EvaluationRisque, self).save(*args, **kwargs)
