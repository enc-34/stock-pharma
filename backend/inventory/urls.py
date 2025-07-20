from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduitViewSet, CategorieViewSet, FournisseurViewSet, MouvementStockViewSet
from .views import alertes_stock_bas, alertes_expiration, dashboard_stats, export_produits_csv, export_produits_pdf

router = DefaultRouter()
router.register('produits', ProduitViewSet)
router.register('categories', CategorieViewSet)
router.register('fournisseurs', FournisseurViewSet)
router.register('mouvements', MouvementStockViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('alertes/stock-bas/', alertes_stock_bas),
    path('alertes/expiration/', alertes_expiration),
    path('dashboard/stats/', dashboard_stats),
    path('export/produits/csv/', export_produits_csv),
    path('export/produits/pdf/', export_produits_pdf),
]
