from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from django.template.loader import render_to_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, F
from .models import Produit, Categorie, Fournisseur, MouvementStock
from .serializers import ProduitSerializer, CategorieSerializer, FournisseurSerializer, MouvementStockSerializer
import csv
from django.http import HttpResponse

class ProduitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class FournisseurViewSet(viewsets.ModelViewSet):
    queryset = Fournisseur.objects.all()
    serializer_class = FournisseurSerializer

class MouvementStockViewSet(viewsets.ModelViewSet):
    queryset = MouvementStock.objects.all()
    serializer_class = MouvementStockSerializer

@action(detail=False, methods=['get'], url_path='scan')
def scan(self, request):
    barcode = request.query_params.get('barcode', None)
    if not barcode:
        return Response({"error": "Barcode manquant"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        produit = Produit.objects.get(barcode=barcode)
        serializer = self.get_serializer(produit)
        return Response(serializer.data)
    except Produit.DoesNotExist:
        return Response({"error": "Produit introuvable"}, status=status.HTTP_404_NOT_FOUND)


# ---- ALERTES ----
@api_view(['GET'])
def alertes_stock_bas(request):
    produits = Produit.objects.filter(stock__lte=F('stock_min'))
    serializer = ProduitSerializer(produits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def alertes_expiration(request):
    produits = Produit.objects.filter(date_expiration__lte=timezone.now().date())
    serializer = ProduitSerializer(produits, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def alertes_view(request):
    stock_min = 10  # seuil d'alerte pour le stock
    today = timezone.now().date()
    expiration_limit = today + timezone.timedelta(days=30)

    stock_bas = Produit.objects.filter(stock__lt=stock_min)
    expiration_proche = Produit.objects.filter(date_expiration__lte=expiration_limit)

    return Response({
        "stock_bas": [{"id": p.id, "nom": p.nom, "stock": p.stock} for p in stock_bas],
        "expiration": [{"id": p.id, "nom": p.nom, "date_expiration": p.date_expiration} for p in expiration_proche]
    })

# ---- DASHBOARD ----
@api_view(['GET'])
def dashboard_stats(request):
    total_produits = Produit.objects.count()
    total_stock = Produit.objects.aggregate(total=Sum('stock'))['total'] or 0
    total_categories = Categorie.objects.count()
    return Response({
        "total_produits": total_produits,
        "total_stock": total_stock,
        "total_categories": total_categories
    })

# ---- EXPORT CSV ----
@api_view(['GET'])
def export_produits_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prix', 'Stock', 'Date expiration'])
    for p in Produit.objects.all():
        writer.writerow([p.nom, p.prix, p.stock, p.date_expiration])
    return response

# ---- EXPORT PDF ----
@api_view(['GET'])
def export_produits_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produits.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    y = 750
    p.setFont("Helvetica", 12)
    p.drawString(100, y, "Liste des Produits")
    y -= 30
    for produit in Produit.objects.all():
        p.drawString(100, y, f"{produit.nom} - Stock: {produit.stock}")
        y -= 20
    p.showPage()
    p.save()
    return response