$(document).ready(function() {
    $('.form-eliminar').on('submit', function(event) {
        event.preventDefault();
        
        let form = $(this);
        let libroCodigo = form.data('libro-codigo');
        let numeroReserva = form.data('numero-reserva');
        let csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();

        if (!numeroReserva) {
            console.error('Número de reserva no definido');
            return;
        }

        Swal.fire({
            title: '¿Estás seguro?',
            text: "No podrás revertir esto.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: `/portal_adm/mantenedor_reservas/detalle_reserva/${numeroReserva}/eliminar_detalle/`,
                    data: {
                        libro_codigo: libroCodigo,
                        csrfmiddlewaretoken: csrfToken
                    },
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Eliminado',
                                text: response.message,
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