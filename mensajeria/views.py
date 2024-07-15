from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import datetime


class Cuenta:
    def __init__(self, numero, nombre, saldo, NumerosContacto):
        self.nombre = nombre
        self.numero = numero
        self.saldo = int(saldo)
        self.numerosContacto = NumerosContacto
        self.historial = []


BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]


def encontrar_cuenta(numero):
    for cuenta in BD:
        if cuenta.numero == numero:
            return cuenta
    return None


@require_GET
def contactos(request):
    minumero = request.GET.get('minumero')
    cuenta = encontrar_cuenta(minumero)
    if cuenta:
        contactos_info = {contacto: encontrar_cuenta(contacto).nombre for contacto in cuenta.contactos}
        return JsonResponse(contactos_info)
    return JsonResponse({"error": "Cuenta no encontrada"}, status=404)


@require_POST
def pagar(request):
    minumero = request.GET.get('minumero')
    numerodestino = request.GET.get('numerodestino')
    valor = float(request.GET.get('valor'))
    cuenta_origen = encontrar_cuenta(minumero)
    cuenta_destino = encontrar_cuenta(numerodestino)
    if cuenta_origen and cuenta_destino:
        if cuenta_origen.saldo >= valor:
            cuenta_origen.saldo -= valor
            cuenta_destino.saldo += valor
            fecha = datetime.datetime.now().strftime("%d/%m/%Y")
            cuenta_origen.historial.append(f"Pago realizado de {valor} a {cuenta_destino.nombre} en {fecha}")
            cuenta_destino.historial.append(f"Pago recibido de {valor} de {cuenta_origen.nombre} en {fecha}")
            return JsonResponse({"status": "Realizado", "fecha": fecha})
        return JsonResponse({"error": "Saldo insuficiente"}, status=400)
    return JsonResponse({"error": "Cuenta no encontrada"}, status=404)


@require_GET
def historial(request):
    minumero = request.GET.get('minumero')
    cuenta = encontrar_cuenta(minumero)
    if cuenta:
        return JsonResponse({
            "saldo": cuenta.saldo,
            "historial": cuenta.historial
        })
    return JsonResponse({"error": "Cuenta no encontrada"}, status=404)
