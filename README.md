# FinalSoftw

P1.- profe tuvimos un problema con la creacion del modelo de la base de datos, no nos permitia modificarlo las columnas, espero verifique la logica, y nos considere.  

P2.- test no se pudo probar pero pusimos posibles test

P3.-

1. Agregar un campo adicional en la clase Cuenta para rastrear el monto total transferido en un día:

- Añadir un campo monto_transferido_hoy para mantener un registro de la cantidad total de dinero transferido en el día actual.
- Añadir un campo ultima_fecha_transferencia para registrar la fecha de la última transferencia.


    class Cuenta(models.Model):
        numero = models.CharField(max_length=10, unique=True)
        nombre = models.CharField(max_length=100)
        saldo = models.DecimalField(max_digits=10, decimal_places=2)
        contactos = models.ManyToManyField('self', symmetrical=False, related_name='mis_contactos')
        monto_transferido_hoy = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        ultima_fecha_transferencia = models.DateField(null=True, blank=True)

    def _str_(self):
        return self.nombre

2. Modificar el método pagar para incluir la verificación del límite diario:

    - Verificar si la fecha de la última transferencia es diferente a la fecha actual. Si es diferente, restablecer monto_transferido_hoy a 0.
    - Verificar si monto_transferido_hoy más el valor de la transferencia supera los 200 soles. Si es así, rechazar la transferencia.
    - Si la transferencia es permitida, actualizar monto_transferido_hoy y ultima_fecha_transferencia.
    

    @require_GET
    def pagar(request):
    minumero = request.GET.get('minumero')
    numerodestino = request.GET.get('numerodestino')
    valor = float(request.GET.get('valor'))
    cuenta_origen = get_object_or_404(Cuenta, numero=minumero)
    cuenta_destino = get_object_or_404(Cuenta, numero=numerodestino)

    hoy = datetime.date.today()
    if cuenta_origen.ultima_fecha_transferencia != hoy:
        cuenta_origen.monto_transferido_hoy = 0
        cuenta_origen.ultima_fecha_transferencia = hoy

    if cuenta_origen.monto_transferido_hoy + valor > 200:
        return JsonResponse({"error": "Límite de transferencia diaria excedido"}, status=400)
    
    if cuenta_origen.saldo >= valor:
        cuenta_origen.saldo -= valor
        cuenta_destino.saldo += valor
        cuenta_origen.monto_transferido_hoy += valor
        cuenta_origen.save()
        cuenta_destino.save()
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")
        cuenta_origen.historial.create(descripcion=f"Pago realizado de {valor} a {cuenta_destino.nombre} en {fecha}")
        cuenta_destino.historial.create(descripcion=f"Pago recibido de {valor} de {cuenta_origen.nombre} en {fecha}")
        return JsonResponse({"status": "Realizado", "fecha": fecha})
    return JsonResponse({"error": "Saldo insuficiente"}, status=400)
    
    
Casos de Prueba Nuevos

    1. Caso de éxito: Transferencia dentro del límite diario:
        - Verificar que una transferencia de 150 soles se realice correctamente si el monto transferido hasta ahora es 0.

    2. Caso de éxito: Transferencia que alcanza el límite diario:
        - Verificar que una transferencia de 50 soles se realice correctamente si el monto transferido hasta ahora es 150 soles, alcanzando así el límite de 200 soles.

    3. Caso de error: Transferencia que excede el límite diario:
        - Verificar que una transferencia de 100 soles sea rechazada si el monto transferido hasta ahora es 150 soles.

    4. Caso de error: Transferencia acumulada que excede el límite diario:
       - Verificar que una transferencia de 75 soles sea rechazada si el monto transferido hasta ahora es 150 soles.

    5. Caso de éxito: Transferencia al día siguiente:
       - Verificar que una transferencia de 200 soles se realice correctamente después de que el día haya cambiado y monto_transferido_hoy se haya restablecido.
       
Garantía de que los Casos de Prueba Existentes No Introducen Errores

Los casos de prueba existentes deben seguir funcionando correctamente si están diseñados para verificar las transferencias básicas (saldo suficiente, contactos válidos, etc.). Sin embargo, se deben revisar y posiblemente actualizar los casos de prueba para incluir las nuevas reglas del límite diario. Específicamente, los casos de prueba existentes para la funcionalidad de pagar deben seguir funcionando sin cambios si el límite diario no se alcanza.

Adicionalmente, es recomendable incluir pruebas de regresión para asegurar que las funcionalidades previas no se vean afectadas por el nuevo límite diario.