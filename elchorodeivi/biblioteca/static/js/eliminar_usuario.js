$(document).ready(function() {
    $('.btn-eliminar-usuario').click(function(event) {
        event.preventDefault();

        let usuarioId = $(this).data('usuario-id');
        let url = '/portal_adm/mantenedor_usuarios/eliminar_usuario/' + usuarioId + '/';

        Swal.fire({
            title: 'Eliminar usuario',
            text: "¿Estás seguro de eliminar este usuario? No podrás revertir este proceso.",
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
                                title: 'Usuario eliminado',
                                text: 'El usuario fue eliminado con éxito.',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                location.reload();
                            });
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: 'Hubo un error al eliminar el usuario.',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    },
                    error: function(xhr, errmsg, err) {
                        Swal.fire({
                            title: 'Error',
                            text: 'Hubo un error al eliminar el usuario.',
                            icon: 'error'
                        });
                    }
                });
            }
        });
    });
});