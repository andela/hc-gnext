$(document).ready(function() {
    $("#id_content").markdown();
    $('#id_categories').multiselect({enableFiltering: true});
    $('ul.errorlist').addClass('list-unstyled small');
    $('ul.errorlist li').addClass('text-danger');

});