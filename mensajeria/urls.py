from django.urls import path
from .views import contactos, pagar, historial

urlpatterns = [
    path('contactos/' , contactos, name='contactos'),
    path('pagar/' , pagar, name='pagar'),
    path('historial/' , historial, name='historial'),
]  