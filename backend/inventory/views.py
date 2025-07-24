from rest_framework import viewsets
from .models import Categorie, Fournisseur, Produit, MouvementStock, CommandeFournisseur, HistoriqueVente, ApprovisionnementAuto
from .serializers import (
    CategorieSerializer, FournisseurSerializer, ProduitSerializer, 
    MouvementStockSerializer, CommandeFournisseurSerializer, 
    HistoriqueVenteSerializer, ApprovisionnementAutoSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer


class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all().order_by('nom')
    serializer_class = ProduitSerializer

    @action(detail=False, methods=['get'])
    def critiques(self, request):
        """Retourne les produits avec stock bas ou presque expirés"""
        produits = Produit.objects.filter(stock__lte=models.F('stock_min'))
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)


class MouvementStockViewSet(viewsets.ModelViewSet):
    queryset = MouvementStock.objects.all()
    serializer_class = MouvementStockSerializer


from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from rest_framework.decorators import action
from rest_framework.response import Response

class CommandeFournisseurViewSet(viewsets.ModelViewSet):
    queryset = CommandeFournisseur.objects.all()
    serializer_class = CommandeFournisseurSerializer

    @action(detail=True, methods=['get'], url_path='pdf')
    def export_pdf(self, request, pk=None):
        commande = self.get_queryset().get(pk=pk)
        # Préparer les données des items pour le template
        items = commande.items.all()
        html_string = render_to_string('commande_fournisseur_pdf.html', {'commande': commande, 'items': items})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="commande_{commande.id}.pdf"'

        pisa_status = pisa.CreatePDF(html_string, dest=response)
        if pisa_status.err:
            return Response({'error': 'Erreur lors de la génération du PDF'}, status=500)
        return response


from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

class HistoriqueVenteViewSet(viewsets.ModelViewSet):
    queryset = HistoriqueVente.objects.all()
    serializer_class = HistoriqueVenteSerializer

    @action(detail=False, methods=['post'])
    def enregistrer_vente(self, request):
        """
        Enregistre une vente et crée un mouvement de stock de type SORTIE.
        Attendu JSON: { "produit": id_produit, "quantite": qte_vendue }
        """
        data = request.data
        produit_id = data.get('produit')
        quantite = data.get('quantite')

        if not produit_id or not quantite:
            return Response({"error": "Produit et quantité sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantite = int(quantite)
            if quantite <= 0:
                return Response({"error": "La quantité doit être positive."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Quantité invalide."}, status=status.HTTP_400_BAD_REQUEST)

        from .models import Produit, HistoriqueVente, MouvementStock

        try:
            produit = Produit.objects.get(id=produit_id)
        except Produit.DoesNotExist:
            return Response({"error": "Produit non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        if produit.stock < quantite:
            return Response({"error": "Stock insuffisant."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Créer la vente
            vente = HistoriqueVente.objects.create(
                produit=produit,
                quantite=quantite,
                date_vente=timezone.now()
            )
            # Créer le mouvement de stock SORTIE
            MouvementStock.objects.create(
                produit=produit,
                type_mouvement='SORTIE',
                quantite=quantite,
                date=timezone.now()
            )
            # Mettre à jour le stock du produit
            produit.stock -= quantite
            produit.save()

        serializer = self.get_serializer(vente)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApprovisionnementAutoViewSet(viewsets.ModelViewSet):
    queryset = ApprovisionnementAuto.objects.all().order_by('-date_proposition')
    serializer_class = ApprovisionnementAutoSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

class ApprovisionnementAutoViewSet(viewsets.ModelViewSet):
    queryset = ApprovisionnementAuto.objects.all().order_by('-date_proposition')
    serializer_class = ApprovisionnementAutoSerializer

    @action(detail=True, methods=['post'], url_path='generer-commande')
    def generer_commande(self, request, pk=None):
        approvisionnement = self.get_object()
        commande = approvisionnement.generer_commande()
        if commande:
            return Response({"status": "Commande générée", "commande_id": commande.id})
        else:
            return Response({"status": "Commande déjà générée ou produit sans fournisseur"}, status=400)


