from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


#MODELO BIBLIOTECA

#USUARIO
class Usuario(AbstractUser):
    rut         = models.CharField(unique=True, max_length=10) #UK no se repite rut
    email       = models.EmailField(unique=True) #UK no se repite correo
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    telefono    = models.IntegerField(blank=True, null=True)
    direccion   = models.CharField(max_length=100, blank=True, null=True)
    comuna      = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.username


#LIBRO
class Libro(models.Model):
    codigo          = models.IntegerField(primary_key=True) #IntegerField, ya que el codigo de libro tendrá una nomenclatura especifica
    titulo          = models.CharField(unique=True, max_length=100) #UK, no se repite un libro
    subtitulo       = models.CharField(max_length=100, blank=True, null=True)
    autor           = models.CharField(max_length=100)
    resena          = models.TextField(blank=True, null=True)
    editorial       = models.CharField(max_length=40)

    #9 categorias predefinidas
    CATEGORIAS_LIBRO = [
        ('N', 'Novela'),
        ('P', 'Poesía'),
        ('CU', 'Cuentos'),
        ('D', 'Dramaturgia'),
        ('E', 'Ensayo'),
        ('F', 'Filosofía'),
        ('H', 'Historia'),
        ('A', 'Arte'),
        ('CA', 'Cartas')
    ]

    categoria       = models.CharField(max_length=2, choices=CATEGORIAS_LIBRO)
    portada         = models.ImageField(upload_to='assets/', blank=True, null=True)

    #opciones de estado de libro
    ESTADOS_LIBRO = [
        ('D', 'Disponible'),
        ('R', 'Reservado'),
        ('PR', 'Prestado'),
        ('ER', 'En reparación'),
        ('PE', 'Perdido')
    ]

    estado_libro    = models.CharField(max_length=2, choices=ESTADOS_LIBRO, default='D') #por defecto disponible

    def __str__(self):
        return str(self.titulo)


#RESERVA
class Reserva(models.Model):
    numero_reserva      = models.AutoField(primary_key=True)
    usuario             = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cantidad_libros     = models.IntegerField(default=0) #contador de la cantidad de libros
    fec_creacion        = models.DateTimeField(auto_now_add=True) #sysdate de la reserva cuando se agrega un producto al carrito o recien se crea
    fec_reserva         = models.DateField(blank=True, null=True)
    fec_compromiso      = models.DateField(blank=True, null=True)
    fec_listo_ret       = models.DateField(blank=True, null=True)
    fec_max_ret         = models.DateField(blank=True, null=True)
    fec_retiro          = models.DateField(blank=True, null=True)
    fec_dev_prog        = models.DateField(blank=True, null=True)
    fec_dev_real        = models.DateField(blank=True, null=True)
    fec_cancelacion     = models.DateField(blank=True, null=True)
    ult_actualizacion   = models.DateTimeField(auto_now=True)

    #lista de estados de reserva
    ESTADOS_RESERVA = [
        ('P', 'Pendiente'),
        ('R', 'Reservada'),
        ('LR', 'Lista para retiro'),
        ('CO', 'Retirada'),
        ('D', 'Devuelta'),
        ('CA', 'Cancelada')
    ]

    estado_reserva      = models.CharField(max_length=2, choices=ESTADOS_RESERVA, default='P') #por defecto reservada

    def save(self, *args, **kwargs):
        update_fields = set() #actualiza los campos que requieren doble guardado
        #si la reserva cambia a reservada, se guarda la fecha de reserva
        if self.estado_reserva == 'R' and not self.fec_reserva:
            self.fec_reserva = timezone.now().date()
            update_fields.add('fec_reserva')
        #guarda la fecha de compromiso +2 dias de la fecha reserva
        if self.fec_reserva and not self.fec_compromiso:
            self.fec_compromiso = self.fec_reserva + timedelta(days=2)
            update_fields.add('fec_compromiso')
        #si el estado es listo para retiro pero no hay fecha listo para retiro, se guarda la fecha de hoy en listo para retiro
        if self.estado_reserva == 'LR' and not self.fec_listo_ret:
            self.fec_listo_ret = timezone.now().date()
            update_fields.add('fec_listo_ret')
        #si esta guardada la fecha de retiro pero no hay fecha max de retiro, se guarda la fecha max de retiro + 5 dias
        if self.fec_listo_ret and not self.fec_max_ret:
            self.fec_max_ret = self.fec_listo_ret + timedelta(days=5)
            update_fields.add('fec_max_ret')
        #si estado de reserva es retirada, se guarda la fecha de retiro, fecha de hoy
        if self.estado_reserva == 'CO' and not self.fec_retiro:
            self.fec_retiro = timezone.now().date()
            update_fields.add('fec_retiro')
        #si esta guardad la fecha de retiro y no hay fecha dev programada, se guarda esta ultima +7 dias
        if self.fec_retiro and not self.fec_dev_prog:
            self.fec_dev_prog = self.fec_retiro + timedelta(days=7)
            update_fields.add('fec_dev_prog')
        #si estado es devuelta, se guarda fecha de devolucion a fecha de hoy
        if self.estado_reserva == 'D' and not self.fec_dev_real:
            self.fec_dev_real = timezone.now().date()
            update_fields.add('fec_dev_real')
        #si estado de reserva es cancelada, se guarda fecha de cancelacion a fecha de hoy
        if self.estado_reserva == 'CA' and not self.fec_cancelacion:
            self.fec_cancelacion = timezone.now().date()
            update_fields.add('fec_cancelacion')
        super(Reserva, self).save(*args, **kwargs)
        #verifica si se actualizo algun campo que requiera un segundo guardado
        if update_fields:
            super(Reserva, self).save(update_fields=update_fields)

    def __str__(self):
        return str(self.numero_reserva) + " - " + str(self.usuario)


#DETALLE RESERVA
class DetalleReserva(models.Model):
    id_detalle_reserva  = models.AutoField(primary_key=True)
    reserva             = models.ForeignKey(Reserva, on_delete=models.CASCADE) #FK de reserva
    libro               = models.ForeignKey(Libro, on_delete=models.CASCADE) #FK de libro
    
    #llave unica conjunta de reserva y libro
    class Meta:
        unique_together = ('reserva', 'libro')

    def __str__(self):
        return str(self.reserva) + ' - ' + str(self.libro)


#SEÑALES QUE VINCULAN DETALLERESERVA, RESERVA Y LIBRO
#señal para guardar cantidad_libros si se agrega un libro en detallereserva, y que se actualice estado de libro a reservado
@receiver(post_save, sender=DetalleReserva)
def actualizar_reserva_al_agregar_libro(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            instance.reserva.cantidad_libros += 1
            instance.libro.estado_libro = 'R' #actualiza libro a estado reservado
            instance.libro.save()
            instance.reserva.estado_reserva = 'R' #actualiza reserva a estado reservada
            instance.reserva.save()

#señal para restar 1 a cantidad libros en reserva si se elimina una fila de detallereserva, y devuleve el libro a disponible
@receiver(post_delete, sender=DetalleReserva)
def actualizar_reserva_al_eliminar_libro(sender, instance, **kwargs):
    with transaction.atomic():
        instance.reserva.cantidad_libros -= 1
        instance.libro.estado_libro = 'D' #actualiza libro a estado disponible
        instance.libro.save()
        instance.reserva.save()
        # Verifica si la reserva ya no tiene libros reservados
        if instance.reserva.cantidad_libros == 0:
            instance.reserva.estado_reserva = 'P' #actualiza reserva a estado pendiente
            instance.reserva.save()

#señal para actualizar estado de libros al cambiar estado de reserva
@receiver(post_save, sender=Reserva)
def actualizar_estado_libros(sender, instance, created, **kwargs):
    if not created: #solo actualizar cuando se modifica una reserva existente
        with transaction.atomic():
            if instance.estado_reserva == 'CO': #estado retirada
                for detalle in instance.detallereserva_set.all():
                    detalle.libro.estado_libro = 'PR' #cambiar a Prestado
                    detalle.libro.save()
            elif instance.estado_reserva in ['D', 'CA']: #estado devuelta o cancelada
                for detalle in instance.detallereserva_set.all():
                    detalle.libro.estado_libro = 'D' #cambiar a disponible
                    detalle.libro.save()

@receiver(post_delete, sender=Reserva)
def eliminar_detalles_reserva(sender, instance, **kwargs):
    instance.detallereserva_set.all().delete()
