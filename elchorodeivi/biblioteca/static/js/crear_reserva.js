$(document).ready(function() {
    $('#btn_crearReserva').click(function(event) {
        event.preventDefault();

        let form = $('#form_crearReserva');
        let formData = new FormData(form[0]);

        let usuario = formData.get('usuario');

        if (!usuario) {
            Swal.fire({
                title: 'Usuario',
                text: 'Debes seleccionar un usuario para la reserva.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
            return;
        }

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            headers: {'X-CSRFToken': form.find('input[name="csrfmiddlewaretoken"]').val()},
            success: function(response) {
                console.log(response);
                if (response.success) {
                    Swal.fire({
                        title: 'Reserva creada',
                        text: 'La reserva ha sido creada exitosamente.',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = `/portal_adm/mantenedor_reservas/detalle_reserva/${response.numero_reserva}/`;
                        }
                    });
                } else {
                    let errors = JSON.parse(response.errors);
                    let errorMessage = '';
                    for (let field in errors) {
                        if (errors.hasOwnProperty(field)) {
                            errorMessage += errors[field][0].message + '\n';
                        }
                    }
                    Swal.fire({
                        title: 'Error',
                        text: errorMessage,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            },
            error: function(response) {
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al procesar la solicitud. Por favor, intenta nuevamente.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});