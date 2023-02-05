from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from core.ruleta.models import Ruleta
from .models import Apuesta



# Create your views here.

class ApuestaView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            ruleta = Ruleta.objects.get(id=self.kwargs['pk'])
            if not ruleta.estatus:
                raise Exception('No esta abierta esa Ruleta')
            user_id = request.headers.get('User-Id')
            if not user_id:
                raise Exception('El id de usuario no fue proporcionado')
            numero = request.POST.get('numero')
            color = request.POST.get('color')
            if not numero and not color:
                raise Exception('No se especifico el tipo de apuesta')    
            cantidad = request.POST.get('cantidad')
            if not cantidad:
                raise Exception('La cantidad no fue proporcionada')
            if int(cantidad) == 0:
                raise Exception('No puedes apostar una cantidad igual a 0')
            if int(cantidad) < 0:
                raise Exception('No puedes apostar una cantidad negativa')
            if float(cantidad) > 10000:
                raise Exception('No puedes apostar mas de $10000')
            Apuesta.objects.create(
                ruleta = ruleta,
                usuario = user_id,
                cantidad = cantidad,
                numero = numero,
                color = color
            )
            data['estatus'] = 'Se realizo la apuesta de forma exitosa'
        except Ruleta.DoesNotExist:
            data['error'] = 'No existe una ruleta con ese id'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)