from django.urls import path
from .views import RuletaCreateView,RuletaOpenView,RuletaListView,RuletaCloseView

app_name = 'ruleta'


urlpatterns = [
    path('create/',RuletaCreateView.as_view()),
    path('open/<int:pk>/',RuletaOpenView.as_view()),
    path('list/',RuletaListView.as_view()),
    path('close/<int:pk>/',RuletaCloseView.as_view()),
]