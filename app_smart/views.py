from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from app_smart.models import Sensor
from django.views.generic import TemplateView
import logging
from .forms import CSVUploadForm
import csv

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

    
def abre_index(request):
    mensagem = "OLÁ TURMA, SEJAM FELIZES SEMPRE!"
    return HttpResponse(mensagem)


class CSVUploadView(TemplateView):
    template_name = 'upload.html'


def process_csv_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            csv_file = request.FILES['file']
            
            # Verifica se o arquivo tem a extensão correta
            if not csv_file.name.endswith('.csv'):
                form.add_error('file', 'Este não é um arquivo CSV válido.')
            else:
                # Processa o arquivo CSV
                file_data = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(file_data, delimiter=',')  # Altere para ',' se necessário
                
                for row in reader:
                    try:
                        Sensor.objects.create(
                            tipo=row['tipo'],
                            unidade_medida=row['unidade_medida'] if row['unidade_medida'] else None,
                            latitude=float(row['latitude'].replace(',', '.')),
                            longitude=float(row['longitude'].replace(',', '.')),
                            localizacao=row['localizacao'],
                            responsavel=row['responsavel'] if row['responsavel'] else '',
                            status_operacional=True if row['status_operacional'] == 'True' else False,
                            observacao=row['observacao'] if row['observacao'] else '',
                            mac_address=row['mac_address'] if row['mac_address'] else None
                        )
                    except KeyError as e:
                        print(f"Chave não encontrada: {e} na linha: {row}")  # Exibe o erro e a linha problemática
                
    else:
        form = CSVUploadForm()

    return render(request, 'app_smart/upload.html', {'form': form})

