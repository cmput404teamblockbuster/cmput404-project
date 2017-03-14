import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';

export default class UnFriendToolbar extends React.Component{
    //props: Object { initiator: Object, receiver: Object, status: "status_friendship_pending" }
    render(){
        return(
            <Toolbar>
                <ToolbarGroup>
                    <ToolbarTitle text="You guys are Friend"/>
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="DeFriend(not finished)"/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}