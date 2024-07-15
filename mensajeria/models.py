from django.db import models
import json

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True , primary_key=True)
    saldo = models.CharField(max_length=100)
    NumerosContacto = models.TextField(default='[]')

    def __str__(self):
        return self.nombre
    def historialoperaciones():
        return Operacion.objects.filter(usuario=self)
    def transferir(destino ,valor):
        saldo = int(self.saldo)
        if saldo >= valor:
            saldo -= valor
            self.saldo = saldo
            self.save()
            destino.saldo += valor
            destino.save()
            operacion = Operacion(usuario=self, tipo='Transferencia', monto=valor, saldo=self.saldo, contacto=destino)
            operacion.save()
            return True
        else:
            return False


class Operacion(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    destino = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='destino')
    valor = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tipo