from rest_framework import serializers
from .models import Usuario, Operacion


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'saldo', 'NumerosContacto']

class OperacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operacion
        fields = ['id', 'usuario', 'destino', 'valor', 'fecha']