# Generated by Django 4.1.5 on 2023-03-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Télécharger fichier'),
        ),
    ]
