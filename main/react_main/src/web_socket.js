import randomNumber from 'random_number.js'

//web socket class for react compoents
class Web_Socket{
    ws_scheme = window.location.protocol == "https:" ? "wss" : "ws"
    client_socket=null

    //client_socket_url : url path and parameters
    //calling_component : component using websocket, needs to handle incoming messags with takeMessage function 
    constructor(client_socket_url, calling_component) {
        this.client_socket_url =  this.ws_scheme + '://' + window.location.host + client_socket_url
        this.calling_component = calling_component
        this.setup()
    }

    setup() {
        this.client_socket = new WebSocket(this.client_socket_url);

        this.client_socket.onopen = () => {
            // on connecting, do nothing but log it to the console
            console.log('connected')
            this.sendMessage('get_sessions', {})
          }
      
        this.client_socket.onmessage = evt => {
            //incoming message
            const message = JSON.parse(evt.data).message
            console.log(message)
            this.calling_component.takeMessage(message)   //calling componenent must have takeMessage function
          }
      
        this.client_socket.onclose = () => {
            console.log('disconnected')
            // automatically try to reconnect on connection loss
   
            const timer = setTimeout(() => {
                this.setup()
                }, randomNumber(500, 1500))  
          }
    }    
    
    //send socket message
    //messageType : name of message
    //messageText : body of message
    sendMessage (messageType, messageText) {
        const message = {'messageType': messageType, 'messageText': messageText}
        this.client_socket.send(JSON.stringify(message))
    }
}

export default Web_Socket