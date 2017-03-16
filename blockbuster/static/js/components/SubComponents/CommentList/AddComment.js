import React from 'react'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import AddCommentRequest from '../../Requests/AddCommentRequest'
export default class AddComment extends React.Component{
    //props: refresh: callback function, postid: uuid of the post
    constructor(refresh,postid){
        super(refresh,postid);

        this.state = {text:""};
        this.sendComment = this.sendComment.bind(this);
        this.handleTextChange = this.handleTextChange.bind(this);
        this.remount = this.remount.bind(this);

    }

    handleTextChange(event){
        this.setState({text:event.target.value});
    }

    remount(){
        this.setState({text:""});
        this.props.refresh();
    }

    sendComment(){
        if (this.state.text !== ""){
            AddCommentRequest.send(this.state.text,this.props.postid,this.remount);
        }


    }

    render(){
        return(
            <CardMedia>
                <TextField fullWidth={true} multiLine={true} hintText="Write a comment..." value={this.state.text} onChange={this.handleTextChange}/>

                <FlatButton label='Send' onTouchTap={this.sendComment}/>
            </CardMedia>

        );
    }
}