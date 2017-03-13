import React from 'react'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import ChangeRelationRequest from './ChangeRelationRequest'


export default class RespondToPending extends React.Component{
    //props: refresh: callback function, postid: uuid of the post
    constructor(refresh,relation){
        super(refresh,relation);

        this.handleAccept = this.handleAccept.bind(this);
        this.handleIgnore = this.handleIgnore.bind(this);
        this.remount = this.remount.bind(this);

    }

    remount(){
        this.forceUpdate();
        this.props.refresh();
    }

    handleAccept(){
        //alert("want to befreind user: " + this.props.relation['initiator']['username']);
        ChangeRelationRequest.update(this.props.relation['initiator'], this.props.relation['receiver'],
            "status_friends", this.remount);
    }

    handleIgnore(){
        //alert("want to ignore user: " + this.props.relation['initiator']['username']);
        ChangeRelationRequest.update(this.props.relation['initiator'], this.props.relation['receiver'],
            "status_following", this.remount);
    }

    render(){
        return(
            <div>
                <FlatButton style={{width:'50%'}} label='Accept' onTouchTap={this.handleAccept}/>
                <FlatButton style={{width:'50%'}} label='Ignore' onTouchTap={this.handleIgnore}/>
            </div>

        );
    }
}