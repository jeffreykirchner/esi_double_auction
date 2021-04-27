
import React, { Component } from 'react';
import ReactDOM, { findDOMNode } from 'react-dom';
import Popper from 'popper.js';
import 'bootstrap';
import { Tab } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from 'styles.module.css'; 
import Jquery from 'jquery';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTrashAlt } from '@fortawesome/free-solid-svg-icons';

library.add(faTrashAlt);

import BaseComponent from 'base_react.js';
import Web_Socket from 'libs/web_socket.js';
import AxiosPost from 'libs/axios_post.js';

import ParametersCard from 'staff_session/parameters_card.js'

import parse from 'html-react-parser';
//import HtmlToReactParser from 'html-to-react';

class Staff_Session extends Component{
    constructor(props)
    {
        super(props);

        this.state = {
            session : {parameter_set:{periods : []}
                       },           //list of experiment sessions
            working : true,         //waiting for server response
            connecting : true,
        };

        this.handleInputChange = this.handleInputChange.bind(this);
    }    

    pathname = window.location.pathname;

    web_socket = null;
    websocketPath = null;   //websocketPath component of ws url
    channelKey = null;      //channelKey componnet of ws url  
    pageKey = null;         //page key component of ws url

    componentDidMount() {
        AxiosPost(this.pathname, {action:"getSocket"}, this.takeSetup.bind(this));  
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

        if(!connecting)
        {
            this.web_socket.sendMessage("get_session", {sessionID : this.pageKey});
        }
    }

    //handle form input changes
    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        console.log("handle input change " + name + " " + value)
    
        this.setState({
          [name]: value
        });
      }

    //handle incoming socket message
    takeMessage (message) {

        const messageType = message.messageType;
        const messageData = message.messageData;
        
        console.log(messageType);
        console.log(messageData);

        switch(messageType) {
            case "update_parameter_set":
                
                break;
            case "get_session":
                this.takeGetSession(messageData);
                break;

        }
    }

    //get current list of sessions
    takeGetSession (messageData) {
        this.setState({session : messageData.session, working: false});
    }

    //add period to session
    sendAddPeriod(){
        this.web_socket.sendMessage("send_add_period", {session_id : this.state.session.id});
    }

    sendDeletePeriod(periodId){
        this.web_socket.sendMessage("send_delete_period", {periodId : periodId});
    }

    render() {    
        
        return (
            <div className="row justify-content-lg-center m-4">
                <div className="col col-md-8">
                    <ParametersCard connecting = {this.state.connecting}
                                    parameterSet = {this.state.session.parameter_set}
                                    sendAddPeriod = {this.sendAddPeriod.bind(this)}
                                    sendDeletePeriod = {this.sendDeletePeriod.bind(this)}
                                    working = {this.state.working}/>
                </div>
                <div className="col col-md-4">
                </div>
            </div>            
        );
    }
}



function App() {
  return (
    <div>
      <BaseComponent />
      <Staff_Session />
    </div>
  );
}

ReactDOM.render(
    <App />,
    document.getElementById('base')
  );