# Generated by Django 4.1.6 on 2023-08-23 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='item',
            table='items',
        ),
        migrations.AlterModelTable(
            name='price',
            table='prices',
        ),
        migrations.AlterModelTable(
            name='shop',
            table='kiranashops',
        ),
    ]
