
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
            sessions : [],          //list of experiment sessions
            working : true,         //waiting for server response
            connecting : true,
            number_of_periods : 3,
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
            case "create_session":
                this.takeCreateSession(messageData);
                break;
            case "get_session":
                this.takeGetSession(messageData);
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
    takeGetSession (messageData) {

        this.setState({sessions : messageData.sessions, working: false});
        this.setState({parameterSetForm : parameterSetForm});
        //this.setState({parameterSetForm : });
    }

    //delete selected session
    sendDeleteSession(id){
        this.setState({working:true});
        this.web_socket.sendMessage("delete_session",{"id" : id});
    }

    render() {    
        var tmp = <input type="number" value={this.state.number_of_periods} onChange={this.handleInputChange} name="number_of_periods"></input>;

        return (
            <div className="row justify-content-lg-center m-4">
                <div className="col col-md-8">
                    <ParametersCard connecting = {this.state.connecting}/>
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