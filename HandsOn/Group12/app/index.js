function clearchk(){
    $('input[type="checkbox"]:checked').prop('checked',false);
}

$('input[type="checkbox"]').on("change", function(){
    alert('Checked');
})