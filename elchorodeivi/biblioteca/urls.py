#agregar importaciones
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #INDEX, LOGIN y PAGINA PRINCIPAL
    #index
    path('', views.index, name='index'),
    path('buscar_libros/', views.buscar_libros, name='libros_buscar'), #buscar libros del index
    path('reset_contrasena/', views.reset_contrasena, name='contrasena_reset'), #url del reset
    #registro y usuario
    path('registrarse/', views.registrarse, name='cliente_registrarse'), #url para registrarse como cliente
    path('perfil/', views.perfil, name='usuario_perfil'), #url para que el cliente vea su perfil y modifique datos
    path('cambiar_password', views.cambiar_password, name='cambiar_contrasena'),
    #logins y logout
    path('login_adm/', views.login_adm, name='adm_login'), #formulario y login administrador
    path('portal_adm/', views.portal_adm, name='adm_portal'), #url para portal de administracion
    path('login_cliente/', views.login_cliente, name='cliente_login'), #login de cliente navbar
    path('cierre_sesion/', views.cierre_sesion, name='sesion_cierre'), #url de logout
    path('sin_acceso/', views.sin_acceso, name='sin_permisos'), #url de página sin permisos
    #libros y fichas de libros
    path('libros/', views.libros_lista, name='lista_libros'), #url para ver el listado de libros
    path('libros/<int:codigo>/', views.libro_ficha, name='ficha_libro'), #ficha de cada libro

    #CRUD
    #libros
    path('portal_adm/mantenedor_libros/', views.mantenedor_libros, name='libros_mantenedor'), #url para el mantenedor de libros
    path('portal_adm/mantenedor_libros/crear_libro/', views.crear_libro, name='libro_crear'), #url para crear libro
    path('portal_adm/mantenedor_libros/editar_libro/<int:pk>/', views.editar_libro, name='libro_editar'), #url para editar libro
    path('portal_adm/mantenedor_libros/eliminar_libro/<int:pk>/', views.eliminar_libro, name='libro_eliminar'), #url para eliminar libro
    #usuarios
    path('portal_adm/mantenedor_usuarios/', views.mantenedor_usuarios, name='usuarios_mantenedor'), #url de mantenedor de usuarios
    path('portal_adm/mantenedor_usuarios/crear_usuario/', views.crear_usuario, name='usuario_crear' ), #url para crear usuario
    path('portal_adm/mantenedor_usuarios/editar_usuario/<str:username>/', views.editar_usuario, name='usuario_editar' ), #url para editar usuario
    path('portal_adm/mantenedor_usuarios/eliminar_usuario/<str:username>/', views.eliminar_usuario, name='usuario_eliminar'), #url para eliminar usuario
    #reservas
    path('portal_adm/mantenedor_reservas/', views.mantenedor_reservas, name='reservas_mantenedor'), #mantenedor de reservas
    path('portal_adm/mantenedor_reservas/crear_reserva/', views.crear_reserva, name='reserva_crear'), #url crear reserva
    path('portal_adm/mantenedor_reservas/eliminar_reserva/', views.eliminar_reserva, name='reserva_eliminar'), #url eliminar reserva completa
    path('portal_adm/mantenedor_reservas/detalle_reserva/<int:numero_reserva>/', views.detalle_reserva, name='reserva_detalle'), #url para ver el detalle de la reserva
    path('portal_adm/mantenedor_reservas/detalle_reserva/<int:numero_reserva>/editar_estado_reserva/', views.editar_estado_reserva, name='estado_reserva_editar'), #url para editar el estado de reserva
    path('portal_adm/mantenedor_reservas/detalle_reserva/<int:pk>/agregar_libro/', views.agregar_libro, name='libro_agregar'), #url para agregar libros a la reserva
    path('portal_adm/mantenedor_reservas/detalle_reserva/<int:numero_reserva>/eliminar_detalle/', views.eliminar_detalle, name='detalle_eliminar'), #url para eliminar detalle

    #CLIENTE
    path('agregar_carrito/<int:codigo>/', views.agregar_carrito, name='carrito_agregar'), #agregar al carrito un libro y crear instancia reserva
    path('carrito/', views.carrito, name='reserva_carrito'), #url para revisar el carrito
    path('carrito/eliminar/<int:codigo>/', views.eliminar_del_carrito, name='carrito_eliminar_libro'), #url para eliminar un libro del carrito
    path('carrito/confirmar_reserva/', views.confirmar_reserva, name='reserva_confirmar'), #confirmar reserva (crear todos los detallereserva)
    path('carrito/vaciar_reserva/', views.vaciar_reserva, name='reserva_vaciar'), #url para vaciar la reserva
    path('reservas/', views.reservas, name='cliente_reservas'), #url para visualizar las reservas del cliente
    path('reservas/detalle_reserva_cliente/<int:pk>/', views.detalle_reserva_cliente, name='reserva_detalle_cliente'), #url para que el cliente vea el detalle de su reserva seleccionado
    path('reservas/detalle_reserva_cliente/<int:pk>/cancelar_reserva', views.cancelar_reserva, name='reserva_cancelar'), #url para que el cliente cancele su reserva

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)