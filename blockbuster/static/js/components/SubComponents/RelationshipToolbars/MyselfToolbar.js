import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';

export default class MyselfToolbar extends React.Component{
    //props: Object { author: Object, friend: Object, status: "status_friendship_pending" }
    render(){
        return(
            <Toolbar style={{backgroundColor:'#424242', border:'solid 1px #4FC3F7'}} >
                <ToolbarGroup>
                    <ToolbarTitle text="Friend Request Received" />
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Accept"/>
                    <RaisedButton label="Ignore"/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}