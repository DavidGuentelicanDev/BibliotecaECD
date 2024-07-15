$(document).ready(function() {
    $('#btn_guardarLibro').click(function(event) {
        event.preventDefault();

        let form = $('#form_crearLibro');
        let formData = new FormData(form[0]);

        let codigo = formData.get('codigo');
        let titulo = formData.get('titulo');
        let autor = formData.get('autor');
        let editorial = formData.get('editorial');
        let categoria = formData.get('categoria');
        let estadoLibro = formData.get('estado_libro');

        if (!codigo || !titulo || !autor || !editorial || !categoria || !estadoLibro) {
            Swal.fire({
                title: 'Campos vacíos',
                text: 'Por favor, completa todos los campos obligatorios.',
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
                        title: 'Libro creado',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/portal_adm/mantenedor_libros/';
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