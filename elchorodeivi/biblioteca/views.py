from sqlite3 import IntegrityError
from django import forms
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro, Usuario, Reserva, DetalleReserva
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LibroForm, UsuarioForm, ReservaForm, AgregarLibroForm, RegistroForm, PerfilForm, CambiarPasswordForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.core.paginator import Paginator


#INDEX, LOGIN y ELEMENTOS PRINCIPALES
#index con libro aleatorio
def index(request):
    libro_recomendado = Libro.objects.order_by('?').first()
    return render(request, 'biblioteca/index.html', {'libro_recomendado': libro_recomendado})

#buscar del index
def buscar_libros(request):
    if request.method == 'GET':
        query = request.GET.get('query', '') #obtener lo escrito en el buscador con ajax
        libros = Libro.objects.filter(
            Q(titulo__icontains=query) |
            Q(codigo__icontains=query) |
            Q(autor__icontains=query)
        )[:5] #buscar n libros que coincidan con el termino
        sugerencias = [{'titulo': libro.titulo, 'codigo': libro.codigo} for libro in libros] #preparar las sugerencias
        return JsonResponse({'sugerencias': sugerencias}) #devolver sugerencias como respuesta ajax

#ir a login de administracion y loguearse
def login_adm(request):
    if request.method == 'POST':
        username = request.POST.get('usuarioAdm')
        password = request.POST.get('claveAdm')
        #autentificar usando username y password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return JsonResponse({'success': True, 'message': 'Ingreso exitoso.'})
            else:
                return JsonResponse({'success': False, 'message': 'No tiene permisos para acceder.'})
        else:
            return JsonResponse({'success': False, 'message': 'Credenciales incorrectas.'})
    return render(request, 'biblioteca/login_adm.html')

#funcion para permisos admin solamente
def admin_requerido(user):
    return user.is_staff

#permisos de cliente
def solo_clientes(user):
    return not user.is_staff

#pagina que redirige a mensaje sin permisos
def sin_acceso(request):
    return render(request, 'biblioteca/sin_permisos.html')

#reset
def reset_contrasena(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if Usuario.objects.filter(username=username).exists():
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return render(request, 'biblioteca/reset.html')

#registro de usuario cliente
def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Registro de usuario guardado correctamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al registrar el usuario.', 'errors': errors})
    else:
        form = RegistroForm()
    return render(request, 'biblioteca/registro.html', {'form': form})

#perfil
@login_required
def perfil(request):
    if request.method == 'POST':
        form_perfil = PerfilForm(request.POST, instance=request.user)
        if form_perfil.is_valid():
            if form_perfil.has_changed():
                try:
                    form_perfil.save()
                    return JsonResponse({'success': True, 'message': 'Perfil actualizado correctamente.'})
                except forms.ValidationError as e:
                    errors = form_perfil.errors.as_json()
                    return JsonResponse({'success': False, 'message': str(e), 'errors': errors})
                except IntegrityError as e:
                    return JsonResponse({'success': False, 'message': 'Hubo un error al actualizar el perfil.'})
            else:
                errors = form_perfil.errors.as_json()
                return JsonResponse({'success': False, 'message': 'No se han realizado cambios.', 'errors': errors})
        else:
            errors = form_perfil.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Formulario inválido.', 'errors': errors})
    else:
        form_perfil = PerfilForm(instance=request.user)
    return render(request, 'biblioteca/perfil.html', {'form_perfil': form_perfil})

#cambiar contraseña
@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form_contrasena = CambiarPasswordForm(request.user, request.POST)
        if form_contrasena.is_valid():
            user = form_contrasena.save()
            update_session_auth_hash(request, user) #autoriza el cambio con seguridad hash
            return JsonResponse({'success': True, 'message': 'Password actualizada correctamente.'})
        else:
            errors = form_contrasena.errors.as_json()
            return JsonResponse({'success': False, 'message': 'No se entregaron valores válidos para realizar el cambio.', 'errors': errors})
    else:
        form_contrasena = CambiarPasswordForm(request.user)
    return render(request, 'biblioteca/cambiar_contrasena.html', {'form_contrasena': form_contrasena})

#portal administracion
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def portal_adm(request):
    return render(request, 'biblioteca/portal_adm.html')

#login cliente
def login_cliente(request):
    if request.method == 'POST':
        username = request.POST.get('usuarioCliente')
        password = request.POST.get('claveCliente')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Ingreso exitoso.'})
        else:
            return JsonResponse({'success': False, 'message': 'Credenciales incorrectas.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

#logout
def cierre_sesion(request):
    logout(request)
    return redirect('index')

#listado de libros
def libros_lista(request):
    categoria = request.GET.get('categoria')
    autor = request.GET.get('autor')
    editorial = request.GET.get('editorial')
    libros_list = Libro.objects.all().order_by('titulo')
    if categoria:
        libros_list = libros_list.filter(categoria=categoria)
    if autor:
        libros_list = libros_list.filter(autor=autor)
    if editorial:
        libros_list = libros_list.filter(editorial=editorial)
    paginator = Paginator(libros_list, 20) #muestra n libros por pagina
    page_number = request.GET.get('page')
    libros = paginator.get_page(page_number)
    autores = Libro.objects.values_list('autor', flat=True).distinct().order_by('autor')
    categorias = sorted(Libro.CATEGORIAS_LIBRO, key=lambda x: x[1])
    editoriales = Libro.objects.values_list('editorial', flat=True).distinct().order_by('editorial')
    return render(request, 'biblioteca/lista_libros.html', {
        'libros': libros,
        'autores': autores,
        'categorias': categorias,
        'editoriales': editoriales
    })

#ficha de cada libro
def libro_ficha(request, codigo):
    libro = get_object_or_404(Libro, codigo = codigo)
    return render(request, 'biblioteca/ficha_libro.html', {"libro": libro})


#LIBROS
#mantenedor de libros
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def mantenedor_libros(request):
    libros = Libro.objects.all()
    return render(request, 'biblioteca/mantenedor_libros.html', {"libros": libros})

#crear libro
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def crear_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save(commit=False)
            if 'portada' in request.FILES:
                portada = request.FILES['portada']
                direccion_guardado = FileSystemStorage(location = 'biblioteca/static/assets')
                nombre_archivo = direccion_guardado.save(portada.name, portada)
                portada_URL = 'assets/' + nombre_archivo
                libro.portada = portada_URL
            libro.save()
            return JsonResponse({'success': True, 'message': 'El libro ha sido creado exitosamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al crear el libro.', 'errors': errors})
    else:
        form = LibroForm()
    return render(request, 'biblioteca/crear_libro.html', {'form': form})

#editar libro
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def editar_libro(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save(commit=False)
            if 'portada' in request.FILES:
                portada = request.FILES['portada']
                direccion_guardado = FileSystemStorage(location = 'biblioteca/static/assets')
                nombre_archivo = direccion_guardado.save(portada.name, portada)
                portada_URL = 'assets/' + nombre_archivo
                libro.portada = portada_URL
            libro.save()
            return JsonResponse({'success': True, 'message': 'El libro ha sido editado con éxito.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al editar el libro.', 'errors': errors})
    else:
        form = LibroForm(instance=libro)
    return render(request, 'biblioteca/editar_libro.html', {'form': form, 'libro': libro})

#eliminar libro
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def eliminar_libro(request, pk):
    try:
        libro = Libro.objects.get(codigo=pk)
        libro.delete()
        return JsonResponse({'success': True})
    except Libro.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Libro no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


#USUARIOS
#mantenedor de usuarios
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def mantenedor_usuarios(request):
    usuarios = Usuario.objects.filter(is_staff=False)
    return render(request, 'biblioteca/mantenedor_usuarios.html', {'usuarios': usuarios})

#crear usuarios
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Usuario creado exitosamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al crear el usuario.', 'errors': errors})
    else:
        form = UsuarioForm()
    return render(request, 'biblioteca/crear_usuario.html', {'form': form})

#editar usuarios
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def editar_usuario(request, username):
    usuario = get_object_or_404(Usuario, username=username)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Usuario editado exitosamente.'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al editar el usuario.', 'errors': errors})
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'biblioteca/editar_usuario.html', {'form': form, 'usuario': usuario})

#eliminar usuarios
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def eliminar_usuario(request, username):
    try:
        usuario = get_object_or_404(Usuario, username=username)
        usuario.delete()
        return JsonResponse({'success': True})
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuario no encontrado'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


#RESERVAS
#mantenedor de reservas
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def mantenedor_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'biblioteca/mantenedor_reservas.html', {'reservas': reservas})

#crear reserva
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def crear_reserva(request):
    if request.method == 'POST':
        reserva_form = ReservaForm(request.POST)
        if reserva_form.is_valid():
            reserva = reserva_form.save()
            numero_reserva = reserva.numero_reserva
            return JsonResponse({'success': True, 'numero_reserva': numero_reserva})
        else:
            errors = reserva_form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al crear la reserva.', 'errors': errors})
    else:
        reserva_form = ReservaForm()
    return render(request, 'biblioteca/crear_reserva.html', {'reserva_form': reserva_form})

#eliminar una reserva completa
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def eliminar_reserva(request):
    numero_reserva = request.POST.get('numero_reserva')
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    if reserva.estado_reserva in ['P', 'R']:
        reserva.delete()
        return JsonResponse({'success': True, 'message': 'La reserva ha sido eliminada con éxito.'})
    else:
        return JsonResponse({'success': False, 'message': 'Ya no es posible eliminar la reserva. El cliente debe solicitar la cancelación.'})

#detalle de reserva
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def detalle_reserva(request, numero_reserva):
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    libros_reserva = DetalleReserva.objects.filter(reserva=reserva)
    return render(request, 'biblioteca/detalle_reserva.html', {'reserva': reserva, 'libros_reserva': libros_reserva})

#editar estado de reserva
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def editar_estado_reserva(request, numero_reserva):
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_reserva')
        if nuevo_estado is not None:
            if reserva.estado_reserva != nuevo_estado:
                reserva.estado_reserva = nuevo_estado
                reserva.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'No se realizaron cambios.'})
        else:
            return JsonResponse({'success': False, 'message': 'El nuevo estado no se proporcionó.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})

#agregar libro a la reserva
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def agregar_libro(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        form = AgregarLibroForm(reserva=reserva, data=request.POST)
        if form.is_valid():
            nuevo_detalle = form.save(commit=False)
            nuevo_detalle.reserva = reserva
            try:
                nuevo_detalle.save()
                return JsonResponse({'success': True, 'message': 'Libro agregado correctamente a la reserva.', 'numero_reserva': reserva.numero_reserva})
            except ValidationError as e:
                return JsonResponse({'success': False, 'message': str(e.message_dict['__all__'][0])})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Hubo un error al agregar el libro a la reserva.', 'errors': errors})
    else:
        form = AgregarLibroForm(reserva=reserva)
    return render(request, 'biblioteca/agregar_libro.html', {'form': form, 'reserva': reserva})

#eliminar un registro en detalle reserva
@login_required
@user_passes_test(admin_requerido, login_url='/sin_acceso/')
def eliminar_detalle(request, numero_reserva):
    libro_codigo = request.POST.get('libro_codigo')
    reserva = get_object_or_404(Reserva, numero_reserva=numero_reserva)
    try:
        detalle_reserva = DetalleReserva.objects.get(reserva=reserva, libro__codigo=libro_codigo)
        detalle_reserva.delete()
        return JsonResponse({'success': True, 'message': 'El libro ha sido eliminado de la reserva.'})
    except DetalleReserva.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'No se encontró el libro en la reserva.'})


#METODOS DE CLIENTES
#agregar libros al carrito
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def agregar_carrito(request, codigo):
    usuario = request.user #rescatar usuario autenticado
    reserva_activa, created = Reserva.objects.get_or_create(usuario=usuario, estado_reserva='P')  # Verificar si el usuario tiene una reserva activa
    libro = get_object_or_404(Libro, codigo=codigo)
    #obtener o inicializar la lista de libros en el carrito de la sesión
    if 'carrito' not in request.session:
        request.session['carrito'] = []
    #verificar si el libro ya esta en el carrito
    if libro.codigo not in request.session['carrito']:
        request.session['carrito'].append(libro.codigo)
        request.session.modified = True #marcar la sesion como modificada para asegurarse de que se guarden los cambios
        return JsonResponse({'success': True, 'message': f'Se agregó "{libro.titulo}" al carrito.'})
    else:
        return JsonResponse({'success': False, 'message': f'El libro "{libro.titulo}" ya está en tu carrito.'})

@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def carrito(request):
    usuario = request.user  # Rescatar usuario autenticado
    try:
        reserva_activa = Reserva.objects.get(usuario=usuario, estado_reserva='P')  # Obtener la reserva activa pendiente
    except Reserva.DoesNotExist:
        reserva_activa = None
    # Obtener los códigos de los libros en el carrito desde la sesión
    codigos_libros = request.session.get('carrito', [])
    libros_en_carrito = Libro.objects.filter(codigo__in=codigos_libros)
    return render(request, 'biblioteca/carrito.html', {'libros_en_carrito': libros_en_carrito, 'reserva_activa': reserva_activa})

#eliminar libro del carrito
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def eliminar_del_carrito(request, codigo):
    if 'carrito' in request.session:
        carrito = request.session['carrito']
        if codigo in carrito:
            carrito.remove(codigo)
            request.session['carrito'] = carrito
            request.session.modified = True
            return JsonResponse({'success': True, 'message': 'El libro ha sido eliminado del carrito.'})
        else:
            return JsonResponse({'success': False, 'message': 'El libro no está en el carrito.'})
    else:
        return JsonResponse({'success': False, 'message': 'El carrito está vacío.'})

#confirmar reserva
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def confirmar_reserva(request):
    usuario = request.user
    reserva_activa = get_object_or_404(Reserva, usuario=usuario, estado_reserva='P')
    if request.method == 'POST':
        # Verificar si hay libros en el carrito en la sesión y crear DetalleReserva
        if 'carrito' in request.session:
            for codigo in request.session['carrito']:
                libro = get_object_or_404(Libro, codigo=codigo)
                if not DetalleReserva.objects.filter(reserva=reserva_activa, libro=libro).exists():
                    DetalleReserva.objects.create(reserva=reserva_activa, libro=libro)
            # Limpiar el carrito en la sesión
            del request.session['carrito']
            request.session.modified = True  # Marcar la sesión como modificada para asegurarse de que se guarden los cambios
        # Cambiar el estado de la reserva a 'Reservada'
        reserva_activa.estado_reserva = 'R'
        reserva_activa.save()
        # Obtener detalles de los libros reservados
        detalles_reserva = DetalleReserva.objects.filter(reserva=reserva_activa)
        libros_en_reserva = [{'titulo': detalle.libro.titulo, 'autor': detalle.libro.autor} for detalle in detalles_reserva]
        return JsonResponse({
            'success': True,
            'message': 'Tu reserva ha sido confirmada con éxito.',
            'numero_reserva': reserva_activa.numero_reserva,
            'libros_en_reserva': libros_en_reserva,
            'redirect_url': '/'
        })
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

#vaciar reserva
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def vaciar_reserva(request):
    usuario = request.user
    try:
        reserva_activa = Reserva.objects.get(usuario=usuario, estado_reserva='P')
        reserva_activa.estado_reserva = 'CA'  # Cambiar estado a cancelada
        reserva_activa.save()
    except Reserva.DoesNotExist:
        reserva_activa = None
    #vaciar carrito
    if 'carrito' in request.session:
        del request.session['carrito']
        request.session.modified = True
    return JsonResponse({'success': True, 'message': 'Carrito de reservas vaciado correctamente.'})

#ver reservas de cliente
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def reservas(request):
    usuario = request.user
    reservas_usuario = Reserva.objects.filter(usuario=usuario).exclude(cantidad_libros=0).order_by('numero_reserva')
    return render(request, 'biblioteca/reservas.html', {'reservas': reservas_usuario})

#ver detalle de reserva seleccionada
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def detalle_reserva_cliente(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    detalles = reserva.detallereserva_set.all()
    return render(request, 'biblioteca/detalle_reserva_cliente.html', {'reserva': reserva, 'detalles': detalles})

#cancelar reserva por cliente
@login_required
@user_passes_test(solo_clientes, login_url='/sin_acceso/')
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    #solo se cancelan las reservas en estado reservada o lista para retiro
    if reserva.estado_reserva in ['R', 'LR']:
        reserva.estado_reserva = 'CA'  # Cambiar estado a cancelada
        reserva.save()
        return JsonResponse({'success': True, 'message': 'Reserva cancelada exitosamente.'})
    else:
        return JsonResponse({'success': False, 'message': 'No se puede cancelar esta reserva.'})
