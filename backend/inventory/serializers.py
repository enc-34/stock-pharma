from rest_framework import serializers
from .models import Produit, Categorie, Fournisseur, MouvementStock

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)
    fournisseur = FournisseurSerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Categorie.objects.all(), source='categorie', write_only=True)
    fournisseur_id = serializers.PrimaryKeyRelatedField(
        queryset=Fournisseur.objects.all(), source='fournisseur', write_only=True)

    class Meta:
        model = Produit
        fields = ['id', 'nom', 'prix', 'stock', 'stock_min', 'date_expiration','barcode',
                  'categorie', 'fournisseur', 'categorie_id', 'fournisseur_id']

class MouvementStockSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)
    produit_id = serializers.PrimaryKeyRelatedField(
        queryset=Produit.objects.all(), source='produit', write_only=True)

    class Meta:
        model = MouvementStock
        fields = ['id', 'produit', 'produit_id', 'type_mouvement', 'quantite', 'date']
