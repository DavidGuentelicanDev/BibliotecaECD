$(document).ready(function() {
    $('#btn_editarLibro').click(function(event) {
        event.preventDefault();

        let form = $('#form_editarLibro');
        let codigo = $('#id_codigo').val();
        let titulo = $('#id_titulo').val();
        let autor = $('#id_autor').val();
        let editorial = $('#id_editorial').val();
        let categoria = $('#id_categoria').val();
        let estadoLibro = $('#id_estado_libro').val();

        if (!codigo || !titulo || !autor || !editorial || !categoria || !estadoLibro) {
            Swal.fire({
                title: 'Campos vacíos',
                text: 'Por favor, completa todos los campos obligatorios.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
            return;
        }

        let formData = new FormData(form[0]);

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    Swal.fire({
                        title: 'Libro actualizado',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/portal_adm/mantenedor_libros/';
                        }
                    });
                } else {
                    let errors = response.errors;
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