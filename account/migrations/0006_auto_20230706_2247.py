# Generated by Django 3.2.5 on 2023-07-07 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0005_transferencia_moneda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferencia',
            name='cuenta_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_recibidas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transferencia',
            name='cuenta_origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_enviadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
