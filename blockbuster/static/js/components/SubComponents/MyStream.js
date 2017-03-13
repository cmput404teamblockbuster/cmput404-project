import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import MakePost from './MakePost'
import GetStreamRequest from './GetStreamRequest'

export default class MyStream extends React.Component{
    constructor(props){
        super(props);
        GetStreamRequest.get(()=>{})
    }

    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Stream" iconElementLeft={<div/>}/>
                <ul className="mainList">
                    <li>
                       <MakePost/>
                    </li>
                </ul>
            </Paper>
        );
    }
}