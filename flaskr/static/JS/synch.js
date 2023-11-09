$(document).ready(function(){
    
    var socket = io.connect();

    socket.on('connect', function() {
        socket.emit('connected', {data: 'I\'m connected!'});
    });

    $('input.sync').on('input', function(event) {
        socket.emit('value changed', {who: $(this).attr('id'), data: $(this).val()});
        return false;
    });

    socket.on('update value', function(msg) {
        $('input#'+msg.who).val(msg.data)
    });

});