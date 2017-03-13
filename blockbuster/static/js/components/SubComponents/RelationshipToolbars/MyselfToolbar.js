import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';

export default class MyselfToolbar extends React.Component{
    //props: Object { initiator: Object, receiver: Object, status: "status_friendship_pending" }
    render(){
        return(
            <Toolbar >
                <ToolbarGroup>
                    <ToolbarTitle text="Friend Request Received"/>
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Accept"/>
                    <RaisedButton label="Ignore"/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}