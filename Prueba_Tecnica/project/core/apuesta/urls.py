from django.urls import path
from .views import ApuestaView

app_name = 'apuesta'

urlpatterns = [
    path('create/<int:pk>/',ApuestaView.as_view())
]