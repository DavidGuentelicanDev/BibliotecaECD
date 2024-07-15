$(document).ready(function() {

    //evento de entrada del campo buscar
    $('#txt_buscar').keyup(function() {
        let query = $(this).val(); //obtener el termino de busqueda
        //buscar solo si el largo de la busqueda es mayor o igual a 3
        if (query.length >= 3) {
            buscarLibros(query); //llamar a la funcion para buscar libros
        } else {
            $('#resultado_busqueda').empty(); //vacia el contenedor de busquedas si la consulta es menor a 3 de largo
            $('.sugerencias-container').hide(); //oculta el contenedor si no hay busquedas
        }
    });

    //funcion para buscar libros
    function buscarLibros(query) {
        $.ajax({
            type: 'GET',
            url: '/buscar_libros/',
            data: {'query': query},
            dataType: 'json',
            success: function(response) {
                console.log(response);
                $('#resultado_busqueda').empty(); //vacia el contenedor de sugerencias
                if (response.sugerencias.length > 0) {
                    $.each(response.sugerencias, function(index, sugerencia) {
                        $('#resultado_busqueda').append('<a href="/libros/' + sugerencia.codigo + '" class="sugerencia">' + sugerencia.titulo + '</a>');
                    });
                    $('.sugerencias-container').show(); //muestra el contenedor de sugerencias si hay resultados
                } else {
                    $('.sugerencias-container').hide(); //oculta el contenedor de sugerencias si no hay resultados
                }
            },
            error: function(response) {
                console.log('Error al buscar libros:', response);
            }
        });
    }
});