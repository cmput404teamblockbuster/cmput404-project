import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton'
import EditIcon from 'material-ui/svg-icons/editor/mode-edit'
import DeleteIcon from 'material-ui/svg-icons/action/delete'
import ReactMarkdown from 'react-markdown'
import CommentSection from '../CommentList/CommentSection'
import NameLink from './NameLink'
import GetSinglePostRequest from '../../Requests/GetSinglePostRequest'


export default class PostContainer extends React.Component{
    constructor(object,refresh, me){
        super(object,refresh, me);

        if (this.props.object['contentType']==="text/plain"){
            this.body = <p className="postBody">{this.props.object['content']}</p>
        } else if (this.props.object['contentType']==="text/markdown"){
            this.body = <ReactMarkdown source={this.props.object['content']}/>
        } else {
            this.body = <img className="image" src={this.props.object['content']}/>
        }

        this.deleteAction = this.deleteAction.bind(this);
        this.editAction = this.editAction.bind(this);

        this.buttons = undefined;
        // console.log("Profile Container:")
        if (this.props.me){
            this.buttons = [
                <IconButton key={0} style={{float:'right'}} tooltip="edit" onTouchTap={this.editAction}>
                    <EditIcon/>
                </IconButton>,
                <IconButton key={1} style={{float:'right'}} tooltip="delete" onTouchTap={this.deleteAction}>
                    <DeleteIcon/>
                </IconButton>
            ]
        }
    }

    deleteAction(){
        GetSinglePostRequest.delete(this.props.object.id,(response)=>{
            console.log("in post container, delete:", response)
            this.props.refresh()
        })
    }

    editAction(){
        alert("TODO: Edit")
    }

    render(){
        console.log("post container, the post is:",this.props.object);
        return(
            <li>
                <Card className="textField">
                    <CardHeader title={<NameLink object={this.props.object['author']}/>} >
                        {this.buttons}
                    </CardHeader>
                    <Divider/>
                    <CardActions> </CardActions>
                    <CardText >
                        {this.body}
                    </CardText>
                    <Divider/>
                    <CardMedia>
                        <CommentSection host={this.props.object.author.host} postid={this.props.object['id']} object={this.props.object['comments']} refresh={this.props.refresh}/>
                    </CardMedia>
                </Card>
            </li>
        );
    }
}

PostContainer.propTypes = {
    // the post object
    object: React.PropTypes.object.isRequired,

    // to refresh the parent
    refresh: React.PropTypes.func.isRequired,

    // a boolean if this is my post
    me: React.PropTypes.bool
};