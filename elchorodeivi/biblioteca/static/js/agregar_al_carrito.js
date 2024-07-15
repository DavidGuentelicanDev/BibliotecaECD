$(document).ready(function() {
    $('#form_agregarCarrito').submit(function(event) {
        event.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(data) {
                if (data.success) {
                    console.log(data);
                    Swal.fire({
                        title: '¡Agregado al carrito!',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'OK',
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/libros/';
                        }
                    });
                } else {
                    console.log(data);
                    Swal.fire({
                        title: 'Información',
                        text: data.message,
                        icon: 'info',
                        confirmButtonText: 'OK'
                    });
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al agregar el libro al carrito. Por favor, intenta nuevamente más tarde.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
                console.error(error);
            }
        });
    });
});