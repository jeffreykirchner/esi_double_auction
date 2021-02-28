import React from 'react'

import Popper from 'popper.js'
import 'bootstrap'
import { Tab } from 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from 'styles.module.css'; 
import Jquery from 'jquery'

function TableCell(props)
{
    const c = props.class
    const v = props.value
    const content = (<td className={props.class}>{props.value}</td>)
    return(content );
}

function TableRow(props)
{
    let i = 0

    const content =
        props.data.map((cell) =>
            <TableCell key = {i++} class= {cell.class} value={cell.value}/>
        );

    return(<tr>{content}</tr>);
}

function TableRows(props) {
    const content = props.rows.map((row) =>
            <TableRow key={row.id} id = {row.id} data = {row.data}/>
            );

    return(content);
  }

export default TableRows