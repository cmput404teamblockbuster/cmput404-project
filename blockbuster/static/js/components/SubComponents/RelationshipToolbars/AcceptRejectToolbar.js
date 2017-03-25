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
        ChangeRelationRequest.update(this.props.object['author'],this.props.object['friend'],
            "status_friends",this.props.refresh)
    }

    sendIgnoreRequest(){
        ChangeRelationRequest.update(this.props.object['author'],this.props.object['friend'],
            "status_following",this.props.refresh)
    }
    //props: Object { author: Object, friend: Object, status: "status_friendship_pending" }
    render(){
        return(
            <Toolbar >
                <ToolbarGroup>
                    <ToolbarTitle text="Friend Request Received"/>
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Accept" onTouchTap={this.sendAcceptRequest}/>
                    <RaisedButton label="Ignore" onTouchTap={this.sendIgnoreRequest}/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}