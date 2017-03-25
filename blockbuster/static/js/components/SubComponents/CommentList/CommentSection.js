import React from 'react'
import Comment from './Comment'
import AddComment from './AddComment'
import Divider from 'material-ui/Divider'

export default class CommentSection extends React.Component{
    // props: object: a list of object,  postid
    constructor(object,refresh,postid){
        super(object,refresh,postid);
        this.state = {comments: this.props.object.map((comment)=>
            <Comment key={comment['id']} object={comment} /> )};

        this.refresh = this.refresh.bind(this);
    }

    refresh(){
        this.props.refresh(
            ()=>{this.setState({comments: this.props.object.map((comment)=>
                <Comment key={comment['id']} object={comment} />)})

        });


    }



    render(){
        return(

            <ul className="commentList">
                {this.state.comments}
                <AddComment postid={this.props.postid} refresh={this.refresh}/>
            </ul>
        );
    }
}