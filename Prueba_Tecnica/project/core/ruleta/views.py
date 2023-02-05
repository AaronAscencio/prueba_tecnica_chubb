from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Ruleta
from core.apuesta.models import Apuesta
import random

# Create your views here.

class RuletaCreateView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            ruleta = Ruleta.objects.create()
            data['id'] = ruleta.pk
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class RuletaOpenView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            ruleta = Ruleta.objects.get(id=self.kwargs['pk'])
            if not ruleta.estatus:
                ruleta.estatus = True
                ruleta.save()
            data['estatus'] = ruleta.get_estatus()

        except Ruleta.DoesNotExist:
            data['error'] = 'No existe una ruleta con ese id'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
        
class RuletaListView(View):

    def get(self, request, *args, **kwargs):
        data = []
        for ruleta in Ruleta.objects.all():
            data.append(ruleta.toJSON())
        return JsonResponse(data, safe=False)

class RuletaCloseView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            ruleta = Ruleta.objects.get(id=self.kwargs['pk'])
            if not ruleta.estatus:
                raise Exception('Esa ruleta no se encuentra abierta')
            ruleta.estatus = False
            ruleta.save()
            numero_ganador = random.randint(0, 36)
            data = {'numero_ganador':numero_ganador} 
            apuestas = Apuesta.objects.filter(ruleta = ruleta,numero__isnull=False)
            for apuesta in apuestas:
                if apuesta.numero == numero_ganador:
                    data[apuesta.usuario] = apuesta.cantidad * 5
                    apuesta.cantidad = apuesta.cantidad * 5
                    apuesta.save()
                else:
                    data[apuesta.usuario] = -apuesta.cantidad
            apuestas = Apuesta.objects.filter(ruleta = ruleta,color__isnull=False)
            for apuesta in apuestas:
                if (numero_ganador % 2 == 0 and apuesta.color == 'rojo') or (numero_ganador % 2 != 0 and apuesta.color == 'negro'):
                    data[apuesta.usuario] = apuesta.cantidad * 1.8
                    apuesta.cantidad = apuesta.cantidad * 1.8
                    apuesta.save()
                else:
                    apuesta[apuesta.usuario] = -apuesta.cantidad
        except Ruleta.DoesNotExist:
            data['error'] = 'No existe una ruleta con ese id'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    