$(document).ready(function() {
    $('#btn_loginCliente').click(function(event) {
        event.preventDefault();

        let usuario = $('#txt_usuarioCliente').val().trim();
        let clave = $('#txt_claveCliente').val().trim();
        let url = '/login_cliente/';

        if (usuario === '' || clave === '') {
            Swal.fire({
                title: 'Campos obligatorios',
                text: 'Debes indicar un usuario y una clave válidos para iniciar sesión.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                usuarioCliente: usuario,
                claveCliente: clave,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function(response) {
                console.log(response);
                if (response.success) {
                    Swal.fire({
                        title: 'Ingreso exitoso',
                        text: 'Redirigiendo a la página inicial...',
                        icon: 'success',
                        timer: 1000,
                        showConfirmButton: false,
                        didOpen: () => {
                            Swal.showLoading();
                        },
                        willClose: () => {
                            window.location.href = '/';
                        }
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
            error: function(xhr, errmsg, err) {
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un error al intentar iniciar sesión. Por favor, intenta nuevamente más tarde.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});