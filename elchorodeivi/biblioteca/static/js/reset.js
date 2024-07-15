$(document).ready(function() {
    $('#btn_reset').click(function(event) {

        let correo = $('#txt_correoRegistrado').val().trim();

        if (!correo) {
            Swal.fire({
                icon: 'warning',
                title: 'Campo obligatorio',
                text: 'Por favor ingresa tu correo electrónico registrado.',
                confirmButtonText: 'OK'
            });
            return;
        }

        $.ajax({
            url: '/reset_contrasena/',
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'username': correo
            },
            success: function(response) {
                console.log(response);
                if (response.success) {
                    Swal.fire({
                        title: 'Correo enviado',
                        text: 'Se ha enviado un correo de reseteo de contraseña a tu dirección de correo electrónico.',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/';
                        }
                    })
                } else {
                    Swal.fire({
                        title: 'Correo no encontrado',
                        text: 'El correo electrónico ingresado no se encuentra registrado en nuestra base de datos.',
                        icon: 'info',
                        confirmButtonText: 'OK'
                    })
                }
            },
            error: function(xhr, errmsg, err) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Ocurrió un error al procesar la solicitud. Por favor, inténtalo nuevamente más tarde.',
                });
            }
        });
    });
});