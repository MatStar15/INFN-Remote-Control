labels = {
    start : ['Inizializza Acquisizione Dati!', 'waiting for response', 'started']
}


$(document).ready(function(){

    // console.log(labels['start'] + ' !!!!!!')

    var socket = io.connect();

    socket.on('connect', function() {
        socket.emit('connected', socket.id);
    });

    const start_button = document.getElementById('start');
    start_button.addEventListener("click", start_acquisition);

    // const reset_button = document.getElementById('reset');
    // reset_button.addEventListener("click", reset);

    const image = document.getElementById('image');

    var local_disabled = []

    function disable(id,ext = false){
        element = document.getElementById(id)
        console.log('disabeling ' + id)
        element.disabled = true;
        var off_label = labels[id][2]
        // .slice(-1)
        element.textContent = off_label;
        local_disabled.push(id);
        // console.log('broadcasting')
        if(!ext){
            socket.emit('disabled', id);
        };
        
    }

    function start_acquisition(){
        start_button.textContent = labels['start'][1];
        socket.emit('start');
    }

    function reset(){
        for (id of local_disabled){
            entry = document.getElementById(id);
            entry.disabled = false;
            entry.textContent = labels[id][0];
        }
        console.log('resetting')
    }

    socket.on('update_disabled', function(id){
        // console.log('updating disabled')
        if (! local_disabled.includes(id) && id != ''){
            disable(id, ext = true);
        }
    })

    socket.on('update_picture', function(new_plot){
        path = "/static//IMG/"+ new_plot
        image.src = path
    })


    socket.on('finished', function(){
        console.log('Finished')
        reset()
    })
})