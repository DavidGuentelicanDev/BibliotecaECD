$(document).ready(function() {
    $('.btn_confirmarReserva').click(function(event) {
        event.preventDefault();

        let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
        let formData = $('.form_confirmarReserva').serialize();
        formData += `&csrfmiddlewaretoken=${csrftoken}`;

        //calculo de las fechas asociadas
        let fechaReserva = new Date();
        let fechaCompromiso = new Date();
        fechaCompromiso.setDate(fechaCompromiso.getDate() + 2);

        let reservaSumario = `
            <p><strong>Fecha de reserva:</strong> ${fechaReserva.toLocaleDateString()}</p>
            <p><strong>Fecha de compromiso:</strong> ${fechaCompromiso.toLocaleDateString()}</p>
            <p>Recibirás un correo cuando el libro esté listo para retiro.</p>
            <p>¿Quieres confirmar la reserva?</p>
        `;

        Swal.fire({
            title: 'Confirmación de reserva',
            html: reservaSumario,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Confirmar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: $('.form_confirmarReserva').attr('action'),
                    data: formData,
                    success: function(data) {
                        console.log(data);
                        if (data.success) {
                            //lista de libros
                            let librosLista = '<ul>';
                            data.libros_en_reserva.forEach(function(libro) {
                                librosLista += `<li><strong>Título:</strong> ${libro.titulo}, <strong>Autor:</strong> ${libro.autor}</li>`;
                            });
                            librosLista += '</ul>';

                            //mensaje de confirmacion de reserva
                            let confirmacionReserva = `
                                <p><strong>Número de reserva:</strong> ${data.numero_reserva}</p>
                                <p><strong>Libros reservados:</strong></p>
                                ${librosLista}
                                <p><strong>Fecha de reserva:</strong> ${fechaReserva.toLocaleDateString()}</p>
                                <p><strong>Fecha de compromiso:</strong> ${fechaCompromiso.toLocaleDateString()}</p>
                                <p>Recibirás un correo cuando el libro esté listo para retiro.</p>
                                <p>Tienes 5 días para retirar el libro después de que esté listo para retiro.</p>
                                <p>El plazo de préstamo es de 7 días corridos desde que se retire el libro.</p>
                            `;

                            //sweet alert con la confirmacion de la reserva
                            Swal.fire({
                                title: 'Reserva confirmada',
                                html: confirmacionReserva,
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = data.redirect_url;
                                }
                            });
                        } else {
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
                            text: 'Hubo un problema al confirmar la reserva. Por favor, intenta nuevamente más tarde.',
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