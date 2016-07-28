$(function(){
    $('#id_addgroup').on('click', function(){
        $("#toggle_addgroup").toggleClass('hide');
    })
    $('form').submit(function(event){
        event.preventDefault()
        $.ajax({
          url: '/posts/',
          method: 'post',
          data: $(this).serialize(),
          success: function(serverResponse){
            console.log("Received this from server: ", serverResponse)
            console.log("I should probably put that in the DOM...")
          }
        })
    })
})