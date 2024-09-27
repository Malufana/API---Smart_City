from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
import pandas as pd
from app_smart.API.serializers import CSVFileUploadSerializer
from app_smart.models import Sensor
from django.views.generic import TemplateView
from django.shortcuts import render

    
def abre_index(request):
    mensagem = "OLÁ TURMA, SEJAM FELIZES SEMPRE!"
    return HttpResponse(mensagem)


class CSVUploadFormView(TemplateView):
    template_name = 'upload.html'

def process_csv_upload(request):
    if request.method == 'POST':
        serializer = CSVFileUploadSerializer(data=request.POST, files=request.FILES)

        if serializer.is_valid():
            csv_file = request.FILES.get('file')
            try:
                df = pd.read_csv(csv_file)

                for _, row in df.iterrows():
                    Sensor.objects.create(
                        tipo=row['tipo'],
                        unidade_medida=row['unidade_medida'] if pd.notna(row['unidade_medida']) else None,
                        latitude=float(row['latitude'].replace(',', '.')) if pd.notna(row['latitude']) else None,
                        longitude=float(row['longitude'].replace(',', '.')) if pd.notna(row['longitude']) else None,
                        localizacao=row['localizacao'],
                        responsavel=row['responsavel'] if pd.notna(row['responsavel']) else '',
                        status_operacional=True if row['status_operacional'] == 'True' else False,
                        observacao=row['observacao'] if pd.notna(row['observacao']) else '',
                        mac_address=row['mac_address'] if pd.notna(row['mac_address']) else None
                    )
                return render(request, 'upload.html', {'message': 'Arquivo CSV processado com sucesso!'})
            except Exception as e:
                return render(request, 'upload.html', {'error': str(e)})
        return render(request, 'upload.html', {'errors': serializer.errors})
    return render(request, 'upload.html')


