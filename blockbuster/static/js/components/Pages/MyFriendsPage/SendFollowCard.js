import React from 'react'
import Paper from 'material-ui/Paper'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton'
import ChangeRelationRequest from '../../Requests/ChangeRelationRequest'


export default class SendFollowCard extends React.Component {
    constructor(object) {
        // props: refresh: callback function to re-render 
        super(object);

        this.handleNameChange = this.handleNameChange.bind(this);
    	this.handleUUIDChange = this.handleUUIDChange.bind(this);
        this.handleFollow = this.handleFollow.bind(this);
        this.data = {username:"", uuid:""};
    }

    handleFollow(){
        //alert("Attempting to follow username:" + this.data.username);
         if (this.data.username !== ""){
            ChangeRelationRequest.send(this.data, "status_friendship_pending");
        }
       
    }
    handleNameChange(event){
        this.data.username = event.target.value;

    }
    handleUUIDChange(event){
        this.data.uuid = event.target.value;

    }


    render() {
        return (
            <Card className="textField">
                <CardHeader title={"Follow an author. If they accpet you will become friends!"}/>
                <TextField style={{width:'50%'}} hintStyle={{paddingLeft:'20px'}} 
	            	textareaStyle={{padding:'0px 20px 0px 20px'}} onChange={this.handleNameChange} hintText="Author's Username"/>
	            <TextField style={{width:'50%'}} hintStyle={{paddingLeft:'20px'}} 
	            	textareaStyle={{padding:'0px 20px 0px 20px'}} onChange={this.handleUUIDChange} hintText="Author's UUID"/>
	            <CardMedia>
	            	<FlatButton label="Follow" onTouchTap={this.handleFollow}/>
	            </CardMedia>               
            </Card>
        );
    }
}