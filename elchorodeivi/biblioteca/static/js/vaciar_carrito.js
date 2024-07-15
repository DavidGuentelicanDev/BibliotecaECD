$(document).ready(function() {
    $('.form_vaciarCarrito').submit(function(event) {
        event.preventDefault();

        let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        Swal.fire({
            title: 'Vaciar carrito',
            text: 'Esta acción vaciará tu carrito de reservas. ¿Deseas continuar?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Vaciar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: $(this).attr('action'),
                    data: {
                        csrfmiddlewaretoken: csrftoken
                    },
                    success: function(data) {
                        console.log(data);
                        if (data.success) {
                            Swal.fire({
                                title: 'Carrito vaciado',
                                text: data.message,
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = '/';
                                }
                            });
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: 'Hubo un problema al vaciar el carrito de reservas.',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    },
                    error: function(xhr, status, error) {
                        Swal.fire({
                            title: 'Error',
                            text: 'Hubo un problema al vaciar el carrito de reservas. Por favor, intenta nuevamente más tarde.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                        console.error(error);
                    }
                });
            }
        });
    });
});