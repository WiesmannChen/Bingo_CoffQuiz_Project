// This script is for add like
$(document).ready(function() {
    $('#like_btn').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('data-coffeeid');
        $.get('/coffquiz/like_coffee/',
            {'coffee_id': catecategoryIdVar},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });
});

// this script is for suggest
$('#search-input').keyup(function (){
    var query;
    query = $(this).val();

    $.get('/coffquiz/suggest/',
        {'suggestion':query},
        function (data){
            $('#coffeelist-listing').html(data);
        })
});


