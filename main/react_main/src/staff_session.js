
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
import { faTrashAlt } from '@fortawesome/free-solid-svg-icons';

library.add(faTrashAlt);

import BaseComponent from 'base_react.js';
import Web_Socket from 'libs/web_socket.js';
import AxiosPost from 'libs/axios_post.js';

import ParametersCard from 'staff_session/parameters_card.js'

import parse from 'html-react-parser';

class Staff_Session extends Component{
    state = {
        sessions : [],          //list of experiment sessions
        working : true,         //waiting for server response
        connecting: true
    };

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

    render() {    

        return (
            <div className="row justify-content-lg-center mt-4">
                <div className="col col-md-8">
                    <ParametersCard connecting = {this.state.connecting}/>
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