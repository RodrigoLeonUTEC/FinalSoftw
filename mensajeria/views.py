from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from .models import Cuenta , Operacion
import datetime


def encontrar_cuenta(numero):
    try:
        return Cuenta.objects.get(nombre=numero) 
    except Cuenta.DoesNotExist:
        return None


@require_GET
def contactos(request):
    minumero = request.GET.get('minumero')
    cuenta = encontrar_cuenta(minumero)
    if cuenta:
        contactos_info = {contacto: encontrar_cuenta(contacto).nombre for contacto in cuenta.NumerosContacto}
        return JsonResponse(contactos_info)
    return JsonResponse({"error": "Cuenta no encontrada"}, status=404)


@require_POST
def pagar(request):
    minumero = request.POST.get('minumero')
    numerodestino = request.POST.get('numerodestino')
    valor = float(request.POST.get('valor'))
    cuenta_origen = encontrar_cuenta(minumero)
    cuenta_destino = encontrar_cuenta(numerodestino)
    if cuenta_origen and cuenta_destino:
        if cuenta_origen.saldo >= valor:
            cuenta_origen.saldo -= valor
            cuenta_destino.saldo += valor
            fecha = datetime.datetime.now().strftime("%d/%m/%Y")
            cuenta_origen.historial_operaciones.create(tipo="Pago", valor=valor, fecha=fecha)
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
            "historial": cuenta.historial_operaciones.all()  # Asegúrate de que esto funcione
        })
    return JsonResponse({"error": "Cuenta no encontrada"}, status=404)
