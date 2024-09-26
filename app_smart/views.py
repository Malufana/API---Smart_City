from django.shortcuts import render
from django.http import HttpResponse

def abre_index(request):
    mensagem = "OLÁ TURMA, SEJAM FELIZES SEMPRE!"
    return HttpResponse(mensagem)
