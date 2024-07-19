from django.db import models
from django.contrib import admin
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    address = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()

    def __str__(self):
        return self.name


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name' , 'email' , 'number')
    list_filter =('name' ,)
    search_fields = ['name' , 'number']

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='Document/')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name' ,)
    list_filter = ('name',)
    search_fields = ['name', 'file']


class Donnee(models.Model):
    maturite = models.FloatField()
    risque = models.CharField(max_length=100)
    Reponse = models.CharField(max_length=100)
    id_risque = models.IntegerField()
    occurence = models.FloatField()
    gravite = models.FloatField()
    detection = models.FloatField()
    criticite = models.FloatField()
    recommandation = models.CharField(max_length=100)
    responsable = models.CharField(max_length=100)
    risque_brute = models.FloatField(default=0)
   

def __str__(self):
        return self.risque
    
def save (self, *args, **kwargs):
        # Calcul du champ risque_brute
            self.risque_brute = self.occurence * self.gravite

        # Calcul du champ criticite
            self.criticite = self.risque_brute * self.detection

        # Appel de la méthode save du modèle parent pour enregistrer l'objet
            super().save(*args, **kwargs)

class DonneeAdmin(admin.ModelAdmin):
    list_display = ['maturite', 'risque', 'Reponse', 'id_risque', 'occurence', 'risque_brute', 'detection', 'criticite', 'recommandation', 'responsable', 'gravite']
    list_filter = ('risque',)
    search_fields = ['risque', ]


class Actifs(models.Model):
    class Meta:
        verbose_name = "Actif"
    id = models.ForeignKey(TypeActif, on_delete=models.CASCADE, primary_key=True)
    categorie = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    CPE_id = models.IntegerField()
    Interface_physique = models.CharField(max_length=20)
    Interface_logique = models.CharField(max_length=20)
    #Send_packet ()
    #Receive_packet ()
    
    def __str__(self):
        return f"{self.id}"