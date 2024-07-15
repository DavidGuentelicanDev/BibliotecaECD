$(document).ready(function() {
    $('#filter-btn').click(function() {
        let categoria = $('#categoria-filter').val();
        let autor = $('#autor-filter').val();
        let editorial = $('#editorial-filter').val();
        let url = `?categoria=${categoria}&autor=${autor}&editorial=${editorial}`;
        window.location.href = url;
    });
});