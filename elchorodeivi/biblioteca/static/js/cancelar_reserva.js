$(document).ready(function() {
    $('#btn_cancelarReserva').click(function(event) {
        event.preventDefault();

        let cancelForm = $('.form_cancelarReserva');
        let csrfToken = cancelForm.find('[name=csrfmiddlewaretoken]').val();
        let url = cancelForm.attr('action');

        Swal.fire({
            title: 'Cancelar reserva',
            text: '¿Estás seguro/a de cancelar esta reserva?',
            icon:'warning',
            showCancelButton: true,
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: url,
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Reserva cancelada',
                                text: response.message,
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then(() => {
                                window.location.reload();
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
                            text: 'Ocurrió un error al cancelar la reserva.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                });
            }
        })
    });
});