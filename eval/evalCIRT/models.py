from django.db import models
from django.contrib import admin
from django.db.models.signals import pre_save
from django.dispatch import receiver
from analyse_risques.models import *

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

class PhysicalInterface(models.Model):
    name = models.CharField(max_length=200)
    physical_address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class LogicalInterface(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Actifs(models.Model):
    class Meta:
        verbose_name = "Actifs"
        
    nom = models.ForeignKey(Asset, on_delete=models.CASCADE)
    #categorie = models.ForeignKey(TypeActif, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    cpe_id = models.IntegerField()
    interface_physique = models.ManyToManyField(PhysicalInterface, related_name='actifs')
    interface_logique = models.ManyToManyField(LogicalInterface, related_name='actifs')
    
    def send_packet(self, packet, interface):
        # Logique d'envoi de paquet
        pass

    def receive_packet(self, packet, interface):
        # Logique de réception de paquet
        pass
    
    def __str__(self):
        return f"{self.nom}"  
    