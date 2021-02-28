
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
import Web_Socket from 'web_socket.js'
import TableRows from 'bootstrap_table.js'

import parse from 'html-react-parser';

library.add(fab, faCheckSquare, faCoffee)


class Staff_Home extends Component{
    state = {
        sessions : [],
        working : true
    }

    web_socket = null

    componentDidMount() {  
        this.web_socket = new Web_Socket('/ws/staff-home/fa14d62f-ad50-4a26-bcca-d3bee0daf596/1',this)
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
        this.web_socket.sendMessage("create_session",{})
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
        this.web_socket.sendMessage("delete_session",{"id" : id});
    }

    buildTableJsonCell(className,value){

        return {
            class : className,
            value : value
        }
    }

    buildTableJson(incoming_data){

        let return_data = []

        for(let i=0;i<incoming_data.length;i++)
        {
            let row = {}
            row["id"] = incoming_data[i].id

            let v = incoming_data[i]

            let data = []

            let temp = <a href={'staff_session/' + v.id}>{v.title}</a>
            data.push(this.buildTableJsonCell(styles.table_cell_left, temp))

            temp = v.start_date
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp))
            
            temp = v.current_period
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp))
            
            temp = null
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp))

            temp = <button className='btn btn-outline-danger btn-sm' disabled={this.state.working}
                        onClick={this.sendDeleteSession.bind(this, incoming_data[i].id)}>
                                   Delete
                               </button>
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp))
            
            row["data"] = data

            return_data.push(row)
        }

        console.log(return_data)

        return (return_data)
    }

    render() {   

        const session_table_data = this.buildTableJson(this.state.sessions)

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
                                    {/* <TableRows sessions={this.state.sessions} working={this.state.working} this={this} />               */}
                                    <TableRows rows = {session_table_data} />                                    
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
      <Staff_Home />
    </div>
  );
}

ReactDOM.render(
    <App />,
    document.getElementById('base')
  );