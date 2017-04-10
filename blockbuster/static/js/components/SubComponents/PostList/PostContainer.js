import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import IconButton from 'material-ui/IconButton'
import ShareIcon from 'material-ui/svg-icons/social/people'
import DeleteIcon from 'material-ui/svg-icons/action/delete'
import ReactMarkdown from 'react-markdown'
import CommentSection from '../CommentList/CommentSection'
import NameLink from './NameLink'
import GetSinglePostRequest from '../../Requests/GetSinglePostRequest'
import EditPostDialog from './EditPostDialog'
import moment from 'moment';

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
        this.closeDialog = this.closeDialog.bind(this);

        this.buttons = undefined;
        this.state = {dialog:false};
        if (this.props.me){
            this.buttons = [
                <IconButton key={1} style={{float:'right'}} tooltip="delete" onTouchTap={this.deleteAction}>
                    <DeleteIcon/>
                </IconButton>,
                <IconButton key={0} style={{float:'right'}} tooltip="edit" onTouchTap={this.editAction}>
                    <ShareIcon/>
                </IconButton>,

            ]
        }
    }

    deleteAction(){
        GetSinglePostRequest.delete(this.props.object.id,(response)=>{
            console.log("in post container, delete:", response);
            this.props.refresh()
        })
    }

    editAction(){
        this.setState({dialog: <EditPostDialog closeAction={this.closeDialog} refresh={this.props.refresh} postId={this.props.object.id}/>})
    }

    closeDialog(){
        this.setState({dialog:false})
    }
    render(){
        console.log("post container, the post is:",this.props.object);
        const t_and_d = ((this.props.object.title) && (this.props.object.description)) ?
            <div>
                <CardHeader title={this.props.object.title}
                                subtitle={this.props.object.description}/>
                <Divider/>
            </div>: null;
        return(
            <li>
                <Card className="textField">
                    <CardHeader title={<NameLink object={this.props.object['author']}/>}
                                subtitle={<span>{moment(this.props.object['published']).format("h:mm:ss a, MMMM Do YYYY")}</span>}>
                        {this.buttons}
                    </CardHeader>
                    <Divider/>
                    {t_and_d}
                    <CardText style={{overflow:scroll}}>
                        {this.body}
                    </CardText>
                    <Divider/>
                    <CardMedia>
                        <CommentSection host={this.props.object.author.host} postid={this.props.object['id']} object={this.props.object['comments']} refresh={this.props.refresh}/>
                    </CardMedia>
                    {this.state.dialog}
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