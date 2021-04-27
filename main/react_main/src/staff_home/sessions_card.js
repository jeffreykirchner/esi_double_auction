//session card for staff_home
import React from 'react'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
library.add(faCog, faPlus);

import BootstrapTable from 'libs/bootstrap_table.js';

function SessionCard(props)
{
    const content = (
        <div className="card">
            <div className="card-header">
                <span className="mr-2">Double Auction</span>
                {props.connecting && <span>... Connecting <FontAwesomeIcon icon={faCog} spin /></span>}

                <span className="float-right">
                    <button className="btn btn-outline-success" type="button" onClick={props.sendCreateSession} disabled={props.working}>
                        Create Session <FontAwesomeIcon icon={faPlus} />                               
                    </button>
                </span>                                                                        
            </div>
            <div className="card-body">                            
                <BootstrapTable title = "Sessions" table_data = {props.session_table_data} table_head = {props.session_table_head}/>
            </div>

        </div>
    );

    return(content );
}

export default SessionCard