from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from app_smart.models import Sensor, LuminosidadeData, TemperaturaData, UmidadeData, ContadorData
from django.views.generic import TemplateView
import logging
from .forms import CSVUploadForm
import csv
from dateutil import parser
import pytz
from django import forms

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

class CSVUploadForm(forms.Form):
    sensor_csv = forms.FileField(required=False)
    luminosidade_csv = forms.FileField(required=False)
    temperatura_csv = forms.FileField(required=False)
    umidade_csv = forms.FileField(required=False)
    contador_csv = forms.FileField(required=False)

def process_csv_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        upload_type = request.POST.get('upload_type')
        
        print(request.POST)
        print(request.FILES)
        print(f"Tipo de upload recebido: {upload_type}")


        if form.is_valid():
            if upload_type == 'sensor':
                csv_file = request.FILES.get('sensor_csv')
            elif upload_type == 'luminosidade':
                csv_file = request.FILES.get('luminosidade_csv')
            elif upload_type == 'temperatura':
                csv_file = request.FILES.get('temperatura_csv')
            elif upload_type == 'umidade':
                csv_file = request.FILES.get('umidade_csv')
            elif upload_type == 'contador':
                csv_file = request.FILES.get('contador_csv')
            else:
                form.add_error(None, 'Tipo de upload inválido.')
                return render(request, 'app_smart/upload.html', {'form': form})
        
            # Verifica se o arquivo tem a extensão correta
            if not csv_file.name.endswith('.csv'):
                form.add_error(csv_file.name, 'Este não é um arquivo CSV válido.')
            else:
                
                # Processa o arquivo CSV
                file_data = csv_file.read().decode('ISO-8859-1').splitlines()
                print(file_data)
                reader = csv.DictReader(file_data, delimiter=',')  # Altere para ',' se necessário
                
                
                #Processamento baseado no tipo de upload
                if upload_type == 'sensor': #Processamento de arquivos tipo sensor
                    csv_file = request.FILES.get('sensor_csv')
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

                elif upload_type == 'luminosidade': #Processamento do tipo luminosidade
                    csv_file = request.FILES.get('luminosidade_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            valor = float(row['valor'])
                            timestamp = parser.parse(row['timestamp'])
                            sensor = Sensor.objects.get(id=sensor_id)
                            LuminosidadeData.objects.create(sensor=sensor, valor=valor,
                            timestamp=timestamp)
                            line_count += 1
                            if line_count % 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")

                elif upload_type == 'temperatura':
                    csv_file = request.FILES.get('temperatura_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            valor = float(row['valor'])
                            timestamp = parser.parse(row['timestamp'])
                            sensor = Sensor.objects.get(id=sensor_id)
                            TemperaturaData.objects.create(sensor=sensor, valor=valor, timestamp=timestamp)
                            line_count += 1
                            if line_count% 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")
                        
                elif upload_type == 'umidade':
                    csv_file = request.FILES.get('umidade_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            valor = float(row['valor'])
                            timestamp = parser.parse(row['timestamp']).astimezone(pytz.timezone('America/Sao_Paulo'))
                            sensor = Sensor.objects.get(id=sensor_id)
                            UmidadeData.objects.create(sensor=sensor, valor=valor, timestamp=timestamp)
                            line_count += 1
                            if line_count % 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")

                elif upload_type == 'contador':
                    csv_file = request.FILES.get('contador_csv')
                    line_count = 0
                    for row in reader:
                        try:
                            sensor_id = int(row['sensor_id'])
                            timestamp = parser.parse(row['timestamp'])
                            sensor = Sensor.objects.get(id=sensor_id)
                            ContadorData.objects.create(sensor=sensor, timestamp=timestamp)
                            line_count += 1
                            if line_count % 10000 == 0:
                                print(f"{line_count} linhas processadas...")
                        except KeyError as e:
                            print(f"Chave não encontrada: {e} na linha: {row}")

        else:
            print(form.errors)   

    else:
        form = CSVUploadForm()

    return render(request, 'app_smart/upload.html', {'form': form})

