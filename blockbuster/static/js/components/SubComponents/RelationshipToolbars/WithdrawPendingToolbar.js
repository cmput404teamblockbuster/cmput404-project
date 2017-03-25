import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import ChangeRelationRequest from '../../Requests/ChangeRelationRequest'

export default class WithdrawPendingToolbar extends React.Component{
    //props: Object { author: Object, friend: Object, status: "status_friendship_pending" }
    constructor(object,refresh){
        super(object,refresh);

        this.sendRequest = this.sendRequest.bind(this);
    }

    sendRequest(){
        ChangeRelationRequest.deleteRelation(this.props.object,this.props.refresh)
    }

    render(){
        return(
            <Toolbar >
                <ToolbarGroup>
                    <ToolbarTitle text="Friend Request Sent"/>
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Cancel Friend Request" onTouchTap={this.sendRequest}/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}