# Generated by Django 2.1.8 on 2019-05-12 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0002_newsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('Borrador', 'Borrador'), ('Publicado', 'Publicado')], max_length=10),
        ),
    ]
