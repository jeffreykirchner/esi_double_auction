
import React, { Component } from 'react'

import Popper from 'popper.js'
import 'bootstrap'
import { Tab } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import { AxiosProvider, Request, Get, Delete, Head, Post, Put, Patch, withAxios } from 'react-axios'
import axios from 'axios';

function NavMenu () {
  
    return(

        <div className="nav-item dropdown my-2 my-lg-0">
            <a className="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Menu
            </a>
            <div className="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdown">
                <a className="dropdown-item" href="/admin"  data-placement="bottom" title="Admin Panel">Admin</a>
                <a className="dropdown-item" href="/accounts/logout">Log Out</a>
            </div>
        </div>
    )
    
}

function NavBar(props) {

        var menuJSX

        if(props.isStaff)
        {
            menuJSX = (
                <>
                    <ul className="navbar-nav mr-auto">                                             
                        <li className="nav-item active">
                                       
                        </li>
                        <li className="nav-item active">
                            
                        </li>
                        <li className="nav-item active">
                            
                        </li>

                    </ul>                
                    
                    <NavMenu />      
                </>      
            )    
                    
        }else{
            menuJSX = (
                <ul className="navbar-nav mr-auto">
                    <li className="nav-item active">
                        
                    </li>        
                    <li className="nav-item active">                                 
                        
                    </li>
                </ul>
            )
        }

        return(
            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                {menuJSX}
            </div>
        )
    
}

class BaseComponent extends React.Component {

    state = {isStaff : true}

    componentDidMount() {
        axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
        axios.defaults.xsrfCookieName = "csrftoken"

        axios.post('/', {data:"somedata"})
        .then(
            (result) => {
                console.log(result.data)
            },
            (error) => {
                console.log(error)
            })
        
    }

    render() {
        return(
            <div>
                
                <nav className="navbar navbar-expand-lg navbar-light bg-light">
            
                    <a className="navbar-brand" href="/">
                        ESI
                    </a>
                
                    <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <NavBar isStaff={this.state.isStaff} />
        
                </nav>
                              
            </div>
        )
    }


  }

export default BaseComponent