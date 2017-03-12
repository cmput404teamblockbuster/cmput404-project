import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'

export default class MyProfile extends React.Component{
    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Profile" iconElementLeft={<div/>}/>
            </Paper>
        );
    }
}