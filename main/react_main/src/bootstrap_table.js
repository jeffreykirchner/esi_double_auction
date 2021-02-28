import React from 'react'

import Popper from 'popper.js'
import 'bootstrap'
import { Tab } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from 'styles.module.css'; 
import Jquery from 'jquery'

//take json formatted table cell
//return jsx formatted table cell
function TableCell(props)
{
    const content = (<td className={props.class}>{props.value}</td>);
    return(content );
}

//take table row in json format
//return jsx formatted table row
function TableRow(props)
{
    let i = 0;

    const content =
        props.data.map((cell) =>
            <TableCell key = {i++} class= {cell.class} value={cell.value}/>
        );

    return(<tr>{content}</tr>);
}

//take set of table in json format
//return jsx formatted table
function TableRows(props) {
    const content = props.rows.map((row) =>
            <TableRow key={row.id} id = {row.id} data = {row.data}/>
            );

    return(content);
  }

//take json formatted table cell
//return jsx formatted table cell
function TableHeaderCell(props)
{
    const content = (<th scope="col" className={props.class}>{props.value}</th>);
    return(content );
}

//take json formatted table header
//return jsx table header
function TableHeaderRow(props){
    let i = 0;

    const content =
        props.cells.map((cell) =>
            <TableHeaderCell key = {i++} class= {cell.class} value={cell.value}/>
        );

    return(<tr>{content}</tr>);
}

//takes json formatted table
//returns jsx formatted table
//title : title at top of table
//table_data : array of table row objects
//table_header : array of table head cells
function BootstrapTable(props){

    const content = 
        <table className="table table-hover table-condensed table-responsive-md">                            

            <caption style={{captionSide:'top',textAlign: 'center'}}>{props.title}</caption>

            <thead>
                <TableHeaderRow cells = {props.table_head}/>
            </thead>

            <tbody id="sessionList">                                                  
                <TableRows rows = {props.table_data} />                                    
            </tbody>

        </table>;

    return(content);
}

export default BootstrapTable