//session card for staff_home
import React from 'react'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
library.add(faCog, faPlus);

function ParametersCard(props)
{
    const content = (
        <div className="card">
            <div className="card-header">
                <span className="mr-2">Parameters</span>
                {props.connecting && <span>... Connecting <FontAwesomeIcon icon={faCog} spin /></span>}

                <span className="float-right">
                    
                </span>                                                                        
            </div>
            <div className="card-body">                            
                
            </div>

        </div>
    );

    return(content );
}

export default ParametersCard