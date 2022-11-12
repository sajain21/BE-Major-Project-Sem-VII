const path = require('path');
const http = require('http');
const express = require('express');
const socketio = require('socket.io');
const formatMessage = require('./utils/messages');

const app = express();
const server = http.createServer(app);
const io = socketio(server);
//set static folder
app.use(express.static(path.join(__dirname,'public')));

const botName = "ByExpertise Bot";

//Run when a client connects
io.on('connection', socket => {

    socket.emit('message', formatMessage(botName, 'Welcome to ByExpertise!'));

    //Broadcast when user connects
    socket.broadcast.emit('message', formatMessage(botName, 'A user has joined the chat'));
    //When user disconnects
    socket.on('disconnect',() =>{
        io.emit('message', formatMessage(botName, 'A user has left the chat'));
    });

    //listen for chatMessage
    socket.on('chatMessage', (msg)=>{
        io.emit('message', formatMessage('USER',  msg));
    })
});

const PORT = 3000 || process.env.PORT;

server.listen(PORT, () => console.log(`Server running on port ${PORT}`));
