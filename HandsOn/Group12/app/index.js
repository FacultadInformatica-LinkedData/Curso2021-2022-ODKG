//clear filters
$("#btnclear").on("click", function() {
    $('input[type="checkbox"]:checked').prop('checked',false); //uncheck all checkbox
    $('input[type="radio"]:checked').prop('checked',false); //uncheck all radio
    $('#seldist option').prop('selected', function() {
        return this.defaultSelected;
    });
});

$('input[type="radio"]').on("change", function(){
    filterEvents();
});

