from rest_framework import routers
from .views import (
    CategorieViewSet, FournisseurViewSet, ProduitViewSet, 
    MouvementStockViewSet, CommandeFournisseurViewSet, 
    HistoriqueVenteViewSet, ApprovisionnementAutoViewSet,RegisterView,
)
from .views_export import export_produits_csv, export_produits_pdf
from .views_dashboard import alertes_expiration, dashboard_stats, top5_produits, categories_stats, produits_stock_faible
from django.urls import path



router = routers.DefaultRouter()

router.register(r'categories', CategorieViewSet)
router.register(r'fournisseurs', FournisseurViewSet)
router.register(r'produits', ProduitViewSet)
router.register(r'mouvements', MouvementStockViewSet)
router.register(r'commandes-fournisseurs', CommandeFournisseurViewSet)
router.register(r'ventes', HistoriqueVenteViewSet)
router.register(r'approvisionnements-auto', ApprovisionnementAutoViewSet)

urlpatterns = router.urls + [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('alertes/expiration/', alertes_expiration, name='alertes-expiration'),
    path('alertes/stock_bas/', produits_stock_faible, name='alertes-stock-bas'),
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('dashboard/top5_produits/', top5_produits, name='dashboard-top5-produits'),
    path('dashboard/categories_stats/', categories_stats, name='dashboard-categories-stats'),
    path('export/produits/csv/', export_produits_csv, name='export-produits-csv'),
    path('export/produits/pdf/', export_produits_pdf, name='export-produits-pdf'),
]
