
import React, { Component } from 'react'
import ReactDOM from 'react-dom'
import Popper from 'popper.js'
import 'bootstrap'
import { Tab } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from 'styles.module.css'; 
import Jquery from 'jquery'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { faCheckSquare, faCoffee } from '@fortawesome/free-solid-svg-icons'

import BaseComponent from 'base_react.js'

library.add(fab, faCheckSquare, faCoffee)

// randomNumber = function(minimum,maximum){
//     //return a random number between min and max
//     return (Math.random() * (maximum - minimum + 1) );
// };


const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";

function TableRows(props) {
    const content = props.sessions.map((session) =>
                <tr key={session.id}>
                    <td className={styles.table_cell_left}>
                        <a href={'staff_session/' + session.id}>{session.title}</a>
                    </td>
                    <td className={styles.table_cell_center}>{session.start_date}</td>
                    <td className={styles.table_cell_center}>{session.current_period}</td>
                    <td className={styles.table_cell_center}> </td>
                    <td className={styles.table_cell_center}>
                        <button className="btn btn-outline-danger btn-sm" disabled={props.working}
                                onClick={props.this.sendDeleteSession.bind(props.this,session.id)}>
                            Delete 
                        </button>
                    </td>
                </tr>
            );

    return(content);
  }

class Socket extends Component{
    state = {
        sessions : [],
        working : true
    }

    client_socket = new WebSocket(ws_scheme + '://' + window.location.host +           
                             '/ws/staff-home/fa14d62f-ad50-4a26-bcca-d3bee0daf596/1');

    componentDidMount() {
         this.client_socket.onopen = () => {
            // on connecting, do nothing but log it to the console
            console.log('connected')
            this.sendMessage('get_sessions', {})
          }
      
          this.client_socket.onmessage = evt => {
            const message = JSON.parse(evt.data).message
            console.log(message)
            this.takeMessage(message)
          }
      
          this.client_socket.onclose = () => {
            console.log('disconnected')
            // automatically try to reconnect on connection loss
            this.setState({
                //client_socket: new WebSocket(URL),
            })
          }         
       
    }

    //send socket message
    sendMessage (messageType, messageText) {
        const message = {'messageType': messageType, 'messageText': messageText}
        this.client_socket.send(JSON.stringify(message))
    }

    //handle incoming socket message
    takeMessage (message) {

        const messageType = message.messageType
        const messageData = message.messageData
        
        console.log(messageType)
        console.log(messageData)

        switch(messageType) {
            case "create_session":
                this.takeCreateSession(messageData);
                break;
            case "get_sessions":
                this.takeGetSessions(messageData);
                break;

        }
    }

    //create new session
    sendCreateSession(){
        this.setState({working:true})
        this.sendMessage("create_session",{})
    }
    
    //take result of session creation
    takeCreateSession (messageData) {
        this.setState({sessions:messageData.sessions,working:false})
    }

    //get current list of sessions
    takeGetSessions (messageData) {
        this.setState({sessions:messageData.sessions,working:false})
    }

    //delete selected session
    sendDeleteSession(id){
        //delete specified session
        this.setState({working:true})
        this.sendMessage("delete_session",{"id" : id});
    }

    render() {  
        return (
            <div className="row justify-content-lg-center mt-4">
                <div className="col col-md-8">
                    <div className="card">
                        <div className="card-header">
                            Double Auction

                            <span className="float-right">
                                <button className="btn btn-outline-success" type="button" onClick={this.sendCreateSession.bind(this)} disabled={this.state.working}>
                                    Create Session                                   
                                </button>
                            </span>                                                                        
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
                                    <TableRows sessions={this.state.sessions} working={this.state.working} this={this} />                                                    
                                </tbody>

                            </table>

                        </div>

                    </div>
                </div>
            </div>
        )
    }
}



function App() {
  return (
    <div>
      <BaseComponent />
      <Socket />
    </div>
  );
}

ReactDOM.render(
    <App />,
    document.getElementById('base')
  );