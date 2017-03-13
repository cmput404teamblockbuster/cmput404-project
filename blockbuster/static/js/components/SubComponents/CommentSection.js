import React from 'react'
import Comment from './Comment'
import AddComment from './AddComment'
import Divider from 'material-ui/Divider'

export default class CommentSection extends React.Component{
    // props: object: a list of object, refresh: callback, postid
    constructor(object,refresh){
        super(object,refresh);

        this.comments = this.props.object.map((comment)=>
            <Comment key={comment['uuid']} object={comment}/>
        )
    }
    render(){
        return(

            <ul className="commentList">
                {this.comments}
                <AddComment postid={this.props.postid} refresh={this.props.refresh}/>
            </ul>
        );
    }
}