$(function(){
		
	// Empty validation
	$('input[name="quantity"], input[name="igdName"]').on('keyup', function(){
		if ($('input[name="quantity"]').val()!=='' && $('input[name="igdName"]').val()!=='') {
			$('#addIgdBtn').removeAttr('disabled').addClass('enabled');
		}
	})
	$('textarea[name="direction"]').on('keyup',function(){
		if ($(this).val()!=='') {
			$('#saveStep').removeAttr('disabled').addClass('enabled');
		}
	})
	$('textarea[name="direction"]').on('keyup', function(){
		if ($('#addIgdBtn').hasClass('enabled') && $('#saveStep').hasClass('enabled')) {
			$('#submitRecipe').removeAttr('disabled');
		}
	})

	// Add ingredient
	var num = 0;
	$('#addIgdBtn').on('click',function(){
		var igdHtml = '<div class="showIngredients" id="ingredient'+num+'"><input type="text" name="quantity'+num+'" value="'+$('input[name="quantity"]').val()+'"><input type="text" class="test" name="igdName'+num+'" value="'+$('input[name="igdName"]').val()+'"><span class="btn btn-warning btn-sm rmIgd" data-num="'+num+'">Remove</span></div></div>';
		$('#igdDisplay').append(igdHtml);
		$('input[name="quantity"], input[name="igdName"]').val('');
		num ++;
		return num;
		console.log($('.test').attr('name'));
	})
	$('body').on('click','.rmIgd',function(){
		var numThis = $(this).attr('data-num');
		$('#ingredient'+numThis).remove();
	})
	
	// Add step
	var stepNum = 1;
	$('.stepNum').html(stepNum);
	$('#saveStep').on('click',function(){
		var stepHtml = '<div class="showSteps" id="showStep'+stepNum+'"><input type="hidden" name="step_number'+stepNum+'" value="'+stepNum+'"><textarea name="step'+stepNum+'">'+$('textarea[name="direction"]').val()+'</textarea><div class="btn btn-warning btn-sm rmStep" data-num="'+stepNum+'">Remove</div></div>';
		$('#stepDisplay').append(stepHtml);
		$('textarea[name="direction"]').val('');
		stepNum ++;
		return stepNum;
	})
	$('body').on('click','.rmStep',function(){
		var numThis = $(this).attr('data-num');
		$('#showStep'+numThis).remove();
	})
	$('#create_recipe_f').on('submit',function(e){
		e.preventDefault();
		$.ajax({
			url: '/user/create/recipe/process',
      method: 'post',
      data: $(this).serialize(),
      success: function(serverResponse){
        $('#show_recipe').html(serverResponse);
      }
    })
	})
})