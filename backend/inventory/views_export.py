import csv
from io import StringIO, BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Produit

@api_view(['GET'])
def export_produits_csv(request):
    produits = Produit.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prix', 'Stock', 'Stock Min', 'Catégorie', 'Fournisseur', 'Date Expiration'])

    for p in produits:
        writer.writerow([
            p.nom,
            p.prix,
            p.stock,
            p.stock_min,
            p.categorie.nom if p.categorie else '',
            p.fournisseur.nom if p.fournisseur else '',
            p.date_expiration.strftime('%Y-%m-%d') if p.date_expiration else ''
        ])

    return response

@api_view(['GET'])
def export_produits_pdf(request):
    produits = Produit.objects.all()
    html_string = render_to_string('produits_pdf.html', {'produits': produits})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produits.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return Response({'error': 'Erreur lors de la génération du PDF'}, status=500)
    return response
