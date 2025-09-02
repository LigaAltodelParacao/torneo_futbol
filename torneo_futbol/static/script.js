const socket = io();

socket.on('iniciar', data=>{
    console.log('Partido iniciado', data);
});

socket.on('nuevo_evento', data=>{
    console.log('Evento agregado', data);
});
