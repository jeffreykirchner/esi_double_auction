
import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import Popper from 'popper.js'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from 'styles.module.css'; 
import Jquery from 'jquery'
import { Tab } from 'bootstrap';

// randomNumber = function(minimum,maximum){
//     //return a random number between min and max
//     return (Math.random() * (maximum - minimum + 1) );
// };

const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

class Socket extends Component{
    state = {
          
    }

    client_socket = new WebSocket(ws_scheme + '://' + window.location.host +           
                             '/ws/staff-home//1');

    componentDidMount() {
         this.client_socket.onopen = () => {
            // on connecting, do nothing but log it to the console
            console.log('connected')
            this.submitMessage('get_sessions')
          }
      
          this.client_socket.onmessage = evt => {
            // on receiving a message, add it to the list of messages
            const message = JSON.parse(evt.data)
            console.log(message)
            //this.addMessage(message)
          }
      
          this.client_socket.onclose = () => {
            console.log('disconnected')
            // automatically try to reconnect on connection loss
            this.setState({
                //client_socket: new WebSocket(URL),
            })
          }         
       
    }

    submitMessage = messageType => {
        // on submitting the ChatInput form, send the message, add it to the list and reset the input
        const message = {'messageType': messageType, 'messageText': {}}
        this.client_socket.send(JSON.stringify(message))
      }

    render(){
        return null;
    }
}

// doWebSockets = function()
// {
         
                
    
//         chatSocket.onmessage = function(e) {
//             var data = JSON.parse(e.data);                       
//             app.takeMessage(data);
//         };
    
//         chatSocket.onclose = function(e) {
//             console.error('Socket closed, trying to connect ... ');
//             //app.$data.reconnecting=true;
//             window.setTimeout(doWebSockets(), randomNumber(500,1500));            
//         }; 

//         chatSocket.onopen = function(e) {
//             console.log('Socket connected.');     
//            // app.$data.reconnecting=false;   
//             app.handleSocketConnected();                      
//         };                
// };

function TableRows(props) {
    const content = props.sessions.map((session) =>
                <tr key={session.id}>
                    <td className={styles.table_cell_left}>{session.title}</td>
                    <td className={styles.table_cell_center}>{session.start_date}</td>
                    <td className={styles.table_cell_center}>{session.current_period}</td>
                    <td className={styles.table_cell_center}> </td>
                    <td className={styles.table_cell_center}>
                        <button>
                            Delete 
                        </button>
                    </td>
                </tr>
            );

    return(content);
  }

class MyComponent extends React.Component {

    constructor() {
        super();

        this.state = {
            sessions : [{id:1,title:"title", start_date:"start date", current_period:"1"},
                        {id:2,title:"title2", start_date:"start date 2", current_period:"2"}],
            socket : null,
        }
    }

    componentDidMount() {
        // this.state.socket = new socket();
        // this.state.socket.load();
    }

    render() {  
        return (

            <div className="row justify-content-lg-center">
                <div className="col col-md-8">
                    <div className="card">
                        <div className="card-header">
                            car head
                                                                        
                        </div>
                        <div className="card-body">
                            
                            <table className="table table-hover table-condensed table-responsive-md">                            

                                <caption style={{captionSide:'top',textAlign: 'center'}}>Sessions</caption>

                                <thead>
                                    <tr>
                                        <th scope="col">
                                            Title
                                        </th> 
                                        <th scope="col" className={styles.table_head_center}>
                                            Date                             
                                        </th>
                                        <th scope="col" className={styles.table_head_center}>
                                            Current Period
                                        </th>
                                        <th scope="col" className={styles.table_head_center}>
                                            Treatment
                                        </th>                                                      
                                        <th scope="col" className={styles.table_head_center}>
                                            Control
                                        </th>
                                    </tr>
                                </thead>

                                <tbody id="sessionList">                                                  
                                    <TableRows sessions={this.state.sessions} />                                                    
                                </tbody>

                            </table>

                        </div>

                    </div>
                </div>
            </div>
        );
      
      
    }
  }

function App() {
  return (
    <div>
      <Socket />
      <MyComponent />
    </div>
  );
}

ReactDOM.render(
    <App />,
    document.getElementById('root')
  );