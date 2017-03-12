import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'

export default class PostElement extends React.Component{
    constructor(){
        super();

    }
    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Friends" iconElementLeft={<div/>}/>
            </Paper>
        );
    }
}