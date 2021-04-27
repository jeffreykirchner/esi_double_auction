//session card for staff_home
import React from 'react'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
library.add(faCog, faPlus);

function ParametersTablePeriodSubject(props)
{
    const content = props.values.map((value) =>
                    <span className="mr-2" key={value.id}>{value.value_cost}</span>
    );

    return (content);
}

function ParametersTablePeriod(props)
{
    const content = props.subjects.map((subject) =>
        <div className="row" key={subject.id}>
            <div className="col-md" >
                {subject.id_number}
            </div>
            <div className="col-md">
                {subject.subject_type}
            </div>
            <div className="col-md">
                {subject.subject_type == "Seller" ? <span key="buyerseller">Costs: </span> : <span key="buyerseller">Values: </span>}
                <ParametersTablePeriodSubject values = {subject.values}/>
            </div>
        </div>
    );

    return(content);
}

function ParametersTable(props)
{
    const content = props.parameterSet.periods.map((period) =>
    <div key = {period.id}>
        <div className="row">
            <div className="col" >
                Period: {period.number}
            </div>
        </div>

        <div className="row">
            <div className="col">
                <ParametersTablePeriod subjects = {period.subjects}/>
            </div>
        </div>
    </div>
    );

    return(content);
}

function ParametersCard(props)
{
    
    const content = (
        <div className="card">
            <div className="card-header">
                <span className="mr-2">Parameters</span>
                {props.connecting && <span>... Connecting <FontAwesomeIcon icon={faCog} spin /></span>}

                <span className="float-right">
                    <button className="btn btn-outline-success" type="button" onClick={props.sendAddPeriod} disabled={props.working}>
                        Add Period <FontAwesomeIcon icon={faPlus} />                               
                    </button>
                </span>                                                                        
            </div>
            <div className="card-body">    
                <ParametersTable  parameterSet = {props.parameterSet}/>                
            </div>

        </div>
    );

    return(content);
}

export default ParametersCard