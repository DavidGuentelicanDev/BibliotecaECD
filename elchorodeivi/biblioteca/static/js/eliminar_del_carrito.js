$(document).ready(function() {
    $('.form_carritoEliminarLibro').submit(function(event) {
        event.preventDefault();
        
        let form = $(this);
        let actionUrl = form.attr('action');
        
        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: form.serialize(),
            success: function(data) {
                if (data.success) {
                    console.log(data);
                    Swal.fire({
                        title: 'Eliminado del carrito',
                        text: data.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            location.reload();
                        }
                    });
                } else {
                    console.log(data);
                    Swal.fire({
                        title: 'Error',
                        text: data.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al eliminar el libro del carrito. Por favor, intenta nuevamente más tarde.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
                console.error(error);
            }
        });
    });
});