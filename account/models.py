from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
usuario = get_user_model()


class CuentaCorriente(models.Model):
    user = models.ForeignKey(
        usuario, on_delete=models.CASCADE, related_name='ahorros')
    moneda = models.CharField(max_length=3, choices=[(
        'ARS', 'ARS'), ('USD', 'USD'), ('EUR', 'EUR')])
    dinero = models.IntegerField()
    prestamo = models.IntegerField(default=10000)

    def __str__(self):
        return 'cuenta de ' + self.user.username + ' en ' + self.moneda


@receiver(post_save, sender=usuario)
def crear_cuenta_corriente(sender, instance, created, **kwargs):
    if created:
        print('Se ejecutó el receptor de la señal crear_cuenta_corriente')
        request = kwargs.pop('request', None)
        if request:
            print(request)
            moneda_nombre = request.data.get('moneda', 'USD')
            cuenta_corriente = CuentaCorriente.objects.create(
                user=instance, moneda=moneda_nombre, dinero=5000)
            cuenta_corriente.save()


class Transferencia(models.Model):
    cuenta_origen = models.ForeignKey(
        CuentaCorriente, related_name='transferencias_enviadas', on_delete=models.CASCADE
    )
    cuenta_destino = models.ForeignKey(
        CuentaCorriente, related_name='transferencias_recibidas', on_delete=models.CASCADE
    )
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    moneda = models.CharField(max_length=3)

    def __str__(self):
        return f'Transferencia de {self.cuenta_origen.user.username} a {self.cuenta_destino.user.username}'
