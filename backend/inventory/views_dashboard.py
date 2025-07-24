from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Produit, MouvementStock, Categorie
from django.db.models import Sum, F
from datetime import timedelta

@api_view(['GET'])
def alertes_expiration(request):
    today = timezone.now().date()
    soon = today + timedelta(days=30)
    produits_expirant = Produit.objects.filter(date_expiration__range=(today, soon))
    data = [
        {
            'id': p.id,
            'nom': p.nom,
            'date_expiration': p.date_expiration,
            'stock': p.stock
        }
        for p in produits_expirant
    ]
    return Response(data)

@api_view(['GET'])
def produits_stock_faible(request):
    produits_faible_stock = Produit.objects.filter(stock__lte=F('stock_min'))
    data = [
        {
            'id': p.id,
            'nom': p.nom,
            'stock': p.stock,
            'stock_min': p.stock_min
        }
        for p in produits_faible_stock
    ]
    return Response(data)

@api_view(['GET'])
def dashboard_stats(request):
    total_produits = Produit.objects.count()
    total_stock = Produit.objects.aggregate(total=Sum('stock'))['total'] or 0
    total_mouvements = MouvementStock.objects.count()
    total_categories = Categorie.objects.count()
    data = {
        'total_produits': total_produits,
        'total_stock': total_stock,
        'total_mouvements': total_mouvements,
        'total_categories': total_categories,
    }
    return Response(data)

@api_view(['GET'])
def top5_produits(request):
    produits = Produit.objects.annotate(total_vendu=Sum('ventes__quantite')).order_by('-total_vendu')[:5]
    data = [
        {
            'id': p.id,
            'nom': p.nom,
            'total_vendu': p.total_vendu or 0
        }
        for p in produits
    ]
    return Response(data)

@api_view(['GET'])
def categories_stats(request):
    categories = Categorie.objects.all()
    data = []
    for cat in categories:
        total_produits = cat.produit_set.count()
        total_stock = cat.produit_set.aggregate(total=Sum('stock'))['total'] or 0
        data.append({
            'id': cat.id,
            'nom': cat.nom,
            'total_produits': total_produits,
            'total_stock': total_stock,
        })
    return Response(data)
