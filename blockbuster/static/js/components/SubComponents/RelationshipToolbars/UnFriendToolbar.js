import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import ChangeRelationRequest from '../../Requests/ChangeRelationRequest'

export default class UnFriendToolbar extends React.Component{
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
            <Toolbar style={{backgroundColor:'#424242',  border:'solid 1px #4FC3F7'}}>
                <ToolbarGroup >
                    <ToolbarTitle text="Friends"/>
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Unfriend" onTouchTap={this.sendRequest}/>
                </ToolbarGroup>
            </Toolbar>
        );
    }
}