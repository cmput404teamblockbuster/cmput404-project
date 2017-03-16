import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import ChangeRelationRequest from '../../Requests/ChangeRelationRequest'


export default class AcceptRejectToolbar extends React.Component{
    constructor(object,refresh){
        super(object,refresh);

        this.sendAcceptRequest = this.sendAcceptRequest.bind(this);
        this.sendIgnoreRequest = this.sendIgnoreRequest.bind(this);
    }

    sendAcceptRequest(){
        ChangeRelationRequest.update(this.props.object['initiator'],this.props.object['receiver'],
            "status_friends",this.props.refresh)
    }

    sendIgnoreRequest(){
        ChangeRelationRequest.update(this.props.object['initiator'],this.props.object['receiver'],
            "status_following",this.props.refresh)
    }
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