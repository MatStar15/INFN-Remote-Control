

labels = {
    start : ['Inizializza Acquisizione Dati!', 'waiting for response', 'started']
}


$(document).ready(function(){

    // console.log(labels['start'] + ' !!!!!!')

    var socket = io.connect();

    socket.on('connect', function() {
        socket.emit('connected', {data: 'I\'m connected!'});
    });

    const start_button = document.getElementById('start');
    start_button.addEventListener("click", start_acquisition);

    const reset_button = document.getElementById('reset');
    reset_button.addEventListener("click", on_reset);

    var to_reset = []

    function disable(id, origin){
        element = document.getElementById(id)
        element.disabled = true;
        var off_label = labels[id][2]
        // .slice(-1)
        element.textContent = off_label;
        to_reset.push(id)
        if (origin != 'ext') {
            socket.emit('disabled', id)
        }
    }

    function start_acquisition(){
        start_button.textContent = labels['start'][1];
        socket.emit('start');
    }

    function on_reset(){
        for (id of to_reset){
            entry = document.getElementById(id);
            entry.disabled = false;
            entry.textContent = labels[id][0];
        }
    }


    socket.on('update_disabled', function(id){
        disable(id, 'ext')
        console.log('received update')
    })
})