$(document).ready(function() {
    $('.btn-eliminar-libro').click(function(event) {
        event.preventDefault();

        let libroId = $(this).data('libro-id');
        let url = '/portal_adm/mantenedor_libros/eliminar_libro/' + libroId + '/';

        Swal.fire({
            title: 'Eliminar libro',
            text: "¿Estás seguro de eliminar este libro? No podrás revertir este proceso.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {csrfmiddlewaretoken: csrfToken},
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Libro eliminado',
                                text: 'El libro fue eliminado con éxito.',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: 'Hubo un error al eliminar el libro.',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        Swal.fire({
                            title: 'Error!',
                            text: 'Hubo un error al eliminar el libro.',
                            icon: 'error'
                        });
                    }
                });
            }
        });
    });
});