from django.contrib import admin
from .models import CuentaCorriente, Transferencia

# Register your models here.
admin.site.register(CuentaCorriente)
admin.site.register(Transferencia)
