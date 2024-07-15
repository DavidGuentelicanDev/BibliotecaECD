$(document).ready(function() {
    //guardar datos iniciales
    let originalValues = {};
    $('.form_datosPerfil').find('input, select').each(function() {
        originalValues[$(this).attr('name')] = $(this).val();
    });

    $('.btn_guardarCambios').click(function(event) {
        event.preventDefault();

        let form = $('.form_datosPerfil');
        let formData = new FormData(form[0]);

        //validar si tiene cambios
        let cambiosHechos = false;
        for (let key of formData.keys()) {
            if (formData.get(key) !== originalValues[key]) {
                cambiosHechos = true;
                break;
            }
        }

        if (!cambiosHechos) {
            Swal.fire({
                title: 'Sin cambios',
                text: 'No has realizado ningún cambio en los datos del perfil.',
                icon: 'info',
                confirmButtonText: 'OK'
            });
            return;
        }

        //validar campos vacíos
        let nombres = formData.get('first_name');
        let apellidos = formData.get('last_name');
        let rut = formData.get('rut');
        let username = formData.get('username');
        let telefono = formData.get('telefono');
        let direccion = formData.get('direccion');
        let comuna = formData.get('comuna');

        if (!nombres || !apellidos || !rut || !username || !telefono || !direccion || !comuna) {
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
                        title: 'Datos actualizados',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    });
                } else {
                    if (response.errors) {
                        let errors = JSON.parse(response.errors);
                        let errorMessage = '';
                        for (let field in errors) {
                            for (let error of errors[field]) {
                                errorMessage += `${error.message}\n`;
                            }
                        }
                        Swal.fire({
                            title: 'Error',
                            text: errorMessage,
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    } else {
                        Swal.fire({
                            title: 'Error',
                            text: response.message || 'Hubo un error al actualizar el perfil.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                }
            },
            error: function(xhr, status, error) {
                console.error('Error en la petición Ajax:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al procesar la solicitud.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});