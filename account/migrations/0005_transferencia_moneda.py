# Generated by Django 3.2.5 on 2023-07-06 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_transferencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferencia',
            name='moneda',
            field=models.CharField(default='CUR', max_length=3),
            preserve_default=False,
        ),
    ]
