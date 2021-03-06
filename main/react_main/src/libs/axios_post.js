import React from 'react'
import axios from 'axios';
//post data to path and return to callBack function
function AxiosPost(path, data, callBack){
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.xsrfCookieName = "csrftoken";

    axios.post(path, data)
    .then(
        (result) => {
            //console.log(result.data);
            callBack(result.data);
        },
        (error) => {
            console.log(error);
        });
}

export default AxiosPost;