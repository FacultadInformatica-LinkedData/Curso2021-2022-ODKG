function generateCard(){ //Generate default card
    var card = document.createElement('div'); //card
	Object.assign(card, {className: 'card', style:'width: 18rem;'});
	var cardb=document.createElement('div'); //card body
    Object.assign(cardb, {className: 'card-body'});
    //card body elements
    var cardbt=document.createElement('H5'); 
    Object.assign(cardbt, {className: 'card-title'});
    cardbt.appendChild(document.createTextNode('Title'))
    var cardbD=document.createElement('p');
    cardbD.appendChild(document.createTextNode('Date'))
    var cardbF=document.createElement('p');
    cardbF.appendChild(document.createTextNode('Facility'))
    var cardbP=document.createElement('p');
    cardbP.appendChild(document.createTextNode('Price'))
    var cardBtn= document.createElement('a')
    Object.assign(cardBtn, {className: 'btn btn-primary'});
    cardBtn.appendChild(document.createTextNode('Event page'))
    //create card
    cardb.append(cardbt,cardbD,cardbF,cardbP,cardBtn)
    card.append(cardb);
    return card;
}

//clear filters
$("#btnclear").on("click", function() {
    $('input[type="checkbox"]:checked').prop('checked',false); //uncheck all checkbox
    $('#cardrow').empty(); //clear result field
    
    var newcard= generateCard(); //generate new card
    
    $('#cardrow').append(newcard); //paste new card in result field	
});

$('input[type="checkbox"]').on("click", function(){
    $('#cardrow').empty();
    $('#cardrow').append(generateCard());	
    $('#cardrow').append(document.createElement('br'));
    $('#cardrow').append(generateCard());	
});

$('#D1').on("click", function() {
   document.getElementById("hola").innerHTML="le dio";
});

