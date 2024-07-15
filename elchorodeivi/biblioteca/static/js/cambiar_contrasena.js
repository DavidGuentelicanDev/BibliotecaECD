$(document).ready(function() {
    $('.btn_cambiarContrasena').click(function(event) {
        event.preventDefault();

        let form = $('.form_cambiarContrasena');
        let formData = new FormData(form[0]);

        //validacion campos vacios
        let claveVieja = formData.get('old_password');
        let claveNueva1 = formData.get('new_password1');
        let claveNueva2 = formData.get('new_password2');

        if (!claveVieja || !claveNueva1 || !claveNueva2) {
            Swal.fire({
                title: 'Campos obligatorios',
                text: 'Te faltan llenar algunos campos obligatorios.',
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
                        title: 'Contraseña actualizada',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    });
                } else {
                    let errorMessage = '';
                    if (response.errors) {
                        let errors = JSON.parse(response.errors);
                        for (let field in errors) {
                            for (let error of errors[field]) {
                                errorMessage += `${error.message}\n`;
                            }
                        }
                    } else {
                        errorMessage = response.message || 'Hubo un error al actualizar la contraseña.';
                    }
                    Swal.fire({
                        title: 'Error',
                        text: errorMessage,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
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