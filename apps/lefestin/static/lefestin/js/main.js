$(function(){
    $('#id_addgroup').on('click', function(){
        $("#toggle_addgroup, .veil").removeClass('hide');
    })
    $('.veil').on('click', function(){
    	$("#toggle_addgroup, .veil").addClass('hide');
    })
    $('.showGroupForm').on('submit', function(e){
    	e.preventDefault()
    	$.ajax({
    		url: 'showgroup/ind',
    		method: 'post',
    		data: $(this).serialize(),
    		success: function(serverResponse){
    			$('.showGroupInd').html(serverResponse);
    		}
    	})
    })
})