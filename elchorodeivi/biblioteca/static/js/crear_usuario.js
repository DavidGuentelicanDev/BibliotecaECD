$(document).ready(function() {
    $('#btn_guardarUsuario').click(function(event) {
        event.preventDefault();

        let form = $('#form_crearUsuario');
        let formData = new FormData(form[0]);

        let nombres = formData.get('first_name');
        let apellidos = formData.get('last_name');
        let rut = formData.get('rut');
        let correo = formData.get('email');
        let username = formData.get('username');
        let password1 = formData.get('password1');
        let password2 = formData.get('password2');

        if (!nombres || !apellidos || !rut || !correo || !username || !password1 || !password2) {
            Swal.fire({
                title: 'Campos obligatorios',
                text: 'Te faltan llenar algunos campos obligatorios.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
            return;
        }

        //validar formato de email para el campo username
        let emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(username)) {
            Swal.fire({
                title: 'Formato de correo incorrecto',
                text: 'El nombre de usuario debe tener formato de correo electrónico.',
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
                        title: 'Usuario creado',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/portal_adm/mantenedor_usuarios/';
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