$(document).ready(function() {
    $('.form-estado').on('submit', function(event) {
        event.preventDefault();

        let form = $(this);
        let nuevoEstadoTexto = form.find('button[type="submit"]').text();  // Obtener el texto del botón clickeado
        let nuevoEstado;
        
        switch (nuevoEstadoTexto) {  // Mapear el texto del botón al valor del estado
            case 'Lista para retiro':
                nuevoEstado = 'LR';
                break;
            case 'Retirada':
                nuevoEstado = 'CO';
                break;
            case 'Devuelta':
                nuevoEstado = 'D';
                break;
            case 'Cancelar':
                nuevoEstado = 'CA';
                break;
            default:
                nuevoEstado = '';
        }

        let numeroReserva = form.data('numero-reserva');
        let csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();

        Swal.fire({
            title: '¿Estás seguro?',
            text: `¿Quieres cambiar el estado a ${nuevoEstadoTexto}?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, cambiar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: `/portal_adm/mantenedor_reservas/detalle_reserva/${numeroReserva}/editar_estado_reserva/`,
                    data: {
                        estado_reserva: nuevoEstado,
                        csrfmiddlewaretoken: csrfToken
                    },
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Estado cambiado',
                                text: `El estado de la reserva ha sido cambiado a ${nuevoEstadoTexto}.`,
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: response.message,
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    },
                    error: function() {
                        Swal.fire({
                            title: 'Error',
                            text: 'Hubo un problema al procesar la solicitud. Por favor, intenta nuevamente.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                });
            }
        });
    });
});