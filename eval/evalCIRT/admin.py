from django.contrib import admin 
from .models import *
# Register your models here.
admin.site.register(Company , CompanyAdmin)
admin.site.register(Document , DocumentAdmin)
admin.site.register(Donnee, DonneeAdmin)
admin.site.register(PhysicalInterface)
admin.site.register(LogicalInterface)
admin.site.register(Actifs)