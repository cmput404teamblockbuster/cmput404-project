import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import MakePost from '../MyStreamPage/MakePost'
import GetPublicPostsRequest from '../../Requests/GetPublicPostsRequest'
import PostContainer from '../../SubComponents/PostList/PostContainer'
export default class PublicPosts extends React.Component{
    constructor(){
        super();
        this.state = {posts:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
        GetPublicPostsRequest.get(
            (PostList)=>{
                this.setState({posts:PostList.map(
                    (post)=> <PostContainer key={post['id']} object={post} refresh={this.componentWillMount}/>)
                });
                if (callback){
                    callback()
                }
            }
        )
    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="Public Posts" iconElementLeft={<div/>}/>
                <ul className="mainList">
                    {this.state.posts}
                </ul>
            </Paper>
        );
    }
}