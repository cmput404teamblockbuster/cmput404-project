import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import ChangeRelationRequest from '../../Requests/ChangeRelationRequest'

export default class BefriendToolbar extends React.Component{
    //props: friend { friend: Object, status: "status_friendship_pending", id }
    constructor(friend,refresh){
        super(friend,refresh);

        this.sendRequest = this.sendRequest.bind(this);
    }

    sendRequest(){
        ChangeRelationRequest.send(this.props.friend,"status_friendship_pending",this.props.refresh)
    }

    render(){
        return(
            <Toolbar >
                <ToolbarGroup>
                    {/*<ToolbarTitle text="Not A Friend"/>*/}
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Send Friend Request" onTouchTap={this.sendRequest}/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}