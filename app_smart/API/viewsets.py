from django.contrib.auth.models import User
from rest_framework import generics, permissions
from app_smart.API import serializers
from rest_framework.response import Response
from rest_framework import status
from ..models import Sensor
from rest_framework import viewsets
from app_smart.API.filters import SensorFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser
from app_smart.API.serializers import CSVFileUploadSerializer
import pandas as pd
from django.views.generic import TemplateView
from django.shortcuts import render

class CreateUserAPIViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SensorFilter

