from django.contrib import admin
from .models import Company , CompanyAdmin
from .models import Document , DocumentAdmin
from .models import Donnee , DonneeAdmin

# Register your models here.
admin.site.register(Company , CompanyAdmin)
admin.site.register(Document , DocumentAdmin)
admin.site.register(Donnee, DonneeAdmin)