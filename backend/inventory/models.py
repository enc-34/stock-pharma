from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    fiabilite = models.FloatField(default=5.0, help_text="Note de 1 à 10")
    delai_moyen_livraison = models.PositiveIntegerField(default=0, help_text="En jours")

    def __str__(self):
        return self.nom

    def classement(self):
        """Classement simplifié (fiabilité + rapidité)"""
        return round((self.fiabilite * 0.7) + (10 - self.delai_moyen_livraison) * 0.3, 2)

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='produits')
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True,blank=True, related_name='produits')
    prix = models.DecimalField(max_digits=10, decimal_places=2,  default=0.0)
    
    # Gestion du stock
    stock = models.PositiveIntegerField(default=0)
    stock_min = models.PositiveIntegerField(default=10, help_text="Seuil critique avant réapprovisionnement")
    stock_max = models.PositiveIntegerField(default=100, help_text="Quantité max recommandée")
    
    # Date d’expiration
    date_expiration = models.DateField(blank=True, null=True)

    
    # Autres informations
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def est_presque_expire(self):
        return self.date_expiration and self.date_expiration <= timezone.now().date() + timezone.timedelta(days=30)

    def est_stock_bas(self):
        return self.stock <= self.stock_min

    def est_en_rupture(self):
        return self.stock <= 0

    def __str__(self):
        return self.nom


class MouvementStock(models.Model):
    TYPE_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='mouvements')
    type_mouvement = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantite = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"

class CommandeFournisseur(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='commandes')
    reference = models.CharField(max_length=100)
    date_commande = models.DateTimeField(default=timezone.now)
    date_livraison = models.DateTimeField(blank=True, null=True)
    statut = models.CharField(max_length=50, choices=[
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ], default='EN_ATTENTE')

    def en_retard(self):
        """Vérifie si la commande est en retard"""
        return self.statut != 'LIVREE' and self.date_livraison and self.date_livraison < timezone.now()

    def notifier_fournisseur(self):
        """Relance par email si le fournisseur a une adresse"""
        if self.fournisseur.email:
            send_mail(
                f"Relance de commande {self.reference}",
                f"Bonjour {self.fournisseur.nom}, la commande {self.reference} n’a pas encore été livrée.",
                'noreply@votreapp.com',
                [self.fournisseur.email],
                fail_silently=True
            )

class CommandeFournisseurItem(models.Model):
    commande = models.ForeignKey(CommandeFournisseur, on_delete=models.CASCADE, related_name='items')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return f"{self.produit.nom} - {self.quantite} x {self.prix_unitaire}"

class HistoriqueVente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='ventes')
    quantite = models.IntegerField()
    date_vente = models.DateTimeField(default=timezone.now)

class ApprovisionnementAuto(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='approvisionnements_auto')
    quantite_suggeree = models.IntegerField()
    date_proposition = models.DateTimeField(default=timezone.now)
    commande_generee = models.BooleanField(default=False)

    def generer_commande(self):
        if self.produit.fournisseur and not self.commande_generee:
            commande = CommandeFournisseur.objects.create(
                fournisseur=self.produit.fournisseur,
                reference=f"AUTO-{self.produit.nom[:3].upper()}-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                date_commande=timezone.now(),
                statut="EN_ATTENTE"
            )
            # Création de l'item de commande fournisseur lié
            CommandeFournisseurItem.objects.create(
                commande=commande,
                produit=self.produit,
                quantite=self.quantite_suggeree,
                prix_unitaire=self.produit.prix
            )
            self.commande_generee = True
            self.save()
            return commande
        return None
