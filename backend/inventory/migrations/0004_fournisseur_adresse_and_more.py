# Generated by Django 5.1.6 on 2025-07-22 12:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_produit_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='fournisseur',
            name='adresse',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fournisseur',
            name='delai_moyen_livraison',
            field=models.PositiveIntegerField(default=0, help_text='En jours'),
        ),
        migrations.AddField(
            model_name='fournisseur',
            name='fiabilite',
            field=models.FloatField(default=5.0, help_text='Note de 1 à 10'),
        ),
        migrations.AddField(
            model_name='produit',
            name='fournisseur_principal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produits_principaux', to='inventory.fournisseur'),
        ),
        migrations.AddField(
            model_name='produit',
            name='prix_achat',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='produit',
            name='stock_max',
            field=models.PositiveIntegerField(default=100, help_text='Quantité max recommandée'),
        ),
        migrations.AlterField(
            model_name='fournisseur',
            name='contact',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fournisseur',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='fournisseur',
            name='nom',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='produit',
            name='date_expiration',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='nom',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='produit',
            name='stock_min',
            field=models.PositiveIntegerField(default=10, help_text='Seuil critique avant réapprovisionnement'),
        ),
        migrations.CreateModel(
            name='ApprovisionnementAuto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite_suggeree', models.IntegerField()),
                ('date_proposition', models.DateTimeField(default=django.utils.timezone.now)),
                ('commande_generee', models.BooleanField(default=False)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvisionnements_auto', to='inventory.produit')),
            ],
        ),
        migrations.CreateModel(
            name='CommandeFournisseur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=100)),
                ('date_commande', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_livraison', models.DateTimeField(blank=True, null=True)),
                ('statut', models.CharField(choices=[('EN_ATTENTE', 'En attente'), ('EN_COURS', 'En cours'), ('LIVREE', 'Livrée'), ('ANNULEE', 'Annulée')], default='EN_ATTENTE', max_length=50)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='inventory.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueVente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('date_vente', models.DateTimeField(default=django.utils.timezone.now)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventes', to='inventory.produit')),
            ],
        ),
    ]
