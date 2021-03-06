
import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import Popper from 'popper.js';
import 'bootstrap';
import { Tab } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from 'styles.module.css'; 
import Jquery from 'jquery';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { fab } from '@fortawesome/free-brands-svg-icons';
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { faTrashAlt } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
library.add(fab, faCog, faTrashAlt, faPlus);

import BaseComponent from 'base_react.js';
import Web_Socket from 'libs/web_socket.js';
import BootstrapTable from 'libs/bootstrap_table.js';
import AxiosPost from 'libs/axios_post.js';

import parse from 'html-react-parser';




class Staff_Home extends Component{
    state = {
        sessions : [],          //list of experiment sessions
        working : true,         //waiting for server response
        connecting: true
    };

    web_socket = null;
    websocketPath = null;   //websocketPath component of ws url
    channelKey = null;      //channelKey componnet of ws url  
    pageKey = null;         //page key component of ws url

    componentDidMount() {
        AxiosPost("/",{action:"getSocket"},this.takeSetup.bind(this));  
    }

    takeSetup(data){
        //console.log("take Setup: " + data);
        this.websocketPath = data.websocket_path;
        this.channelKey = data.channel_key;
        this.pageKey = data.page_key;
        
        this.web_socket = new Web_Socket('/ws/' + this.websocketPath + '/' + this.channelKey + '/' + this.pageKey,
                                         this.takeMessage.bind(this),
                                         this.takeConnecting.bind(this)); 
    }

    //update websocket connecting status
    takeConnecting(connecting){
        this.setState({connecting : connecting});
    }

    //handle incoming socket message
    takeMessage (message) {

        const messageType = message.messageType;
        const messageData = message.messageData;
        
        console.log(messageType);
        console.log(messageData);

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
        this.setState({working:true});
        this.web_socket.sendMessage("create_session",{});
    }
    
    //take result of session creation
    takeCreateSession (messageData) {
        this.setState({sessions:messageData.sessions,working:false});
    }

    //get current list of sessions
    takeGetSessions (messageData) {
        this.setState({sessions:messageData.sessions,working:false});
    }

    //delete selected session
    sendDeleteSession(id){
        this.setState({working:true});
        this.web_socket.sendMessage("delete_session",{"id" : id});
    }

    buildTableJsonCell(className,value){

        return {
            class : className,
            value : value
        };
    }

    buildTableJson(incoming_data){

        let return_data = [];

        for(let i=0;i<incoming_data.length;i++)
        {
            let row = {};
            row["id"] = incoming_data[i].id;

            let v = incoming_data[i];

            let data = [];

            let temp = <a href={'staff_session/' + v.id}>{v.title}</a>;
            data.push(this.buildTableJsonCell(styles.table_cell_left, temp));

            temp = v.start_date;
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp));
            
            temp = v.current_period;
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp));
            
            temp = null;
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp));

            temp = <button className='btn btn-outline-danger btn-sm' disabled={this.state.working}
                           onClick={this.sendDeleteSession.bind(this, incoming_data[i].id)}>
                                   Delete <FontAwesomeIcon icon={faTrashAlt} />
                               </button>;
            data.push(this.buildTableJsonCell(styles.table_cell_center, temp));
            
            row["data"] = data;

            return_data.push(row);
        }

        //console.log(return_data);

        return (return_data);
    }

    buildTableHeadJson() {
        let return_data = [];

        return_data.push(this.buildTableJsonCell(styles.table_cell_left,"Title"));
        return_data.push(this.buildTableJsonCell(styles.table_cell_center,"Date"));
        return_data.push(this.buildTableJsonCell(styles.table_cell_center," Current Period"));
        return_data.push(this.buildTableJsonCell(styles.table_cell_center," Treatment"));
        return_data.push(this.buildTableJsonCell(styles.table_cell_center," Control"));

        return (return_data);
    }

    render() {   

        const session_table_data = this.buildTableJson(this.state.sessions);
        const session_table_head = this.buildTableHeadJson();        

        return (
            <div className="row justify-content-lg-center mt-4">
                <div className="col col-md-8">
                    <div className="card">
                        <div className="card-header">
                            <span className="mr-2">Double Auction</span>
                            {this.state.connecting && <span>... Connecting <FontAwesomeIcon icon={faCog} spin /></span>}

                            <span className="float-right">
                                <button className="btn btn-outline-success" type="button" onClick={this.sendCreateSession.bind(this)} disabled={this.state.working}>
                                    Create Session <FontAwesomeIcon icon={faPlus} />                               
                                </button>
                            </span>                                                                        
                        </div>
                        <div className="card-body">
                            
                            <BootstrapTable title = "Sessions" table_data = {session_table_data} table_head = {session_table_head}/>

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
      <BaseComponent />
      <Staff_Home />
    </div>
  );
}

ReactDOM.render(
    <App />,
    document.getElementById('base')
  );