$(function(){
    $('#id_addgroup').on('click', function(){
        $("#toggle_addgroup").toggleClass('hide');
    })
    // $('#process_addgroup').on('submit',function(e){
    //     console.log($(this).serialize()+'&GroupImage='+encodeURIComponent($('input[type="file"]')));
    //     e.preventDefault();
    //     $.ajax({
    //         url: '/process_addgroup',
    //         method: 'post',
    //         data: $(this).serialize()+'&GroupImage='+encodeURIComponent($('input[type="file"]')),
    //         success: function(serverResponse){
    //             $('#showgroupdiv').html(serverResponse);
    //         }
    //     })
    // })
})