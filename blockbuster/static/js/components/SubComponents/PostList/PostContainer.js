import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import CommentSection from '../CommentList/CommentSection'
import NameLink from './NameLink'

export default class PostContainer extends React.Component{
    constructor(object,refresh){
        super(object,refresh);

        if (this.props.object['contentType']==="text/plain"){
            this.body = <p className="postBody">{this.props.object['content']}</p>
        } else if (this.props.object['contentType']==="text/markdown"){
            this.body = <p>TODO: markdown display</p>
        } else {
            console.log("post container", this.props.object['contentType'])
            this.body = <img className="image" src={this.props.object['content']}/>
        }
    }


    render(){
        console.log("post container",this.props.object)
        return(
            <li>
                <Card className="textField">
                    {/*<CardHeader title={this.props.object['author']['username']} titleColor={'#82B1FF'} /><Divider/>*/}
                    <CardHeader title={<NameLink object={this.props.object['author']}/>}/><Divider/>
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