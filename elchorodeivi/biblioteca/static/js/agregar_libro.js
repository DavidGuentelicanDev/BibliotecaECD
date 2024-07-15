$(document).ready(function() {
    $('#btn_agregarLibro').click(function(event) {
        event.preventDefault();

        let form = $('#form_agregarLibro');
        let formData = new FormData(form[0]);

        let libro = formData.get('libro');

        if (!libro) {
            Swal.fire({
                title: 'Libro',
                text: 'Debes seleccionar un libro para agregarlo en la reserva.',
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
                        title: 'Libro agregado',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/portal_adm/mantenedor_reservas/detalle_reserva/' + response.numero_reserva + '/';
                        }
                    });
                } else {
                    let errorMessage = response.message + '\n';
                    if (response.errors) {
                        let errors = JSON.parse(response.errors);
                        for (let field in errors) {
                            if (errors.hasOwnProperty(field)) {
                                errorMessage += errors[field][0].message + '\n';
                            }
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