# Generated by Django 5.1.6 on 2025-07-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
