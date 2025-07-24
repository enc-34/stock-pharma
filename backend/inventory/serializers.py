from rest_framework import serializers
from .models import Categorie, Fournisseur, Produit, MouvementStock, CommandeFournisseur, HistoriqueVente, ApprovisionnementAuto, CommandeFournisseurItem

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class FournisseurSerializer(serializers.ModelSerializer):
    classement = serializers.SerializerMethodField()

    class Meta:
        model = Fournisseur
        fields = '__all__'

    def get_classement(self, obj):
        return obj.classement()


class ProduitSerializer(serializers.ModelSerializer):
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    est_stock_bas = serializers.BooleanField(read_only=True)
    est_en_rupture = serializers.BooleanField(read_only=True)
    est_presque_expire = serializers.BooleanField(read_only=True)

    class Meta:
        model = Produit
        fields = '__all__'


class MouvementStockSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    utilisateur = serializers.CharField(source='utilisateur.username', read_only=True, default='N/A')

    class Meta:
        model = MouvementStock
        fields = '__all__'


class CommandeFournisseurItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommandeFournisseurItem
        fields = ['id', 'produit', 'quantite', 'prix_unitaire']

class CommandeFournisseurSerializer(serializers.ModelSerializer):
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    en_retard = serializers.BooleanField(read_only=True)
    items = CommandeFournisseurItemSerializer(many=True, read_only=True)

    class Meta:
        model = CommandeFournisseur
        fields = '__all__'


class HistoriqueVenteSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)

    class Meta:
        model = HistoriqueVente
        fields = '__all__'


class ApprovisionnementAutoSerializer(serializers.ModelSerializer):
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)

    class Meta:
        model = ApprovisionnementAuto
        fields = '__all__'
