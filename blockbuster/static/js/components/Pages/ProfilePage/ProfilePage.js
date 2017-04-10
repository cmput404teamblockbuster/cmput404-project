import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import ProfileCard from './ProfileCard'
import GetHisPostsRequest from '../../Requests/GetHisPostsRequest'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import ExtractIdFromURL from '../../Requests/ExtractIdFromURL'
import PostContainer from '../../SubComponents/PostList/PostContainer'

export default class ProfilePage extends React.Component{
    constructor(object){
        // props: object
        super(object);

    }

    componentWillMount(callback){
        console.log("Profile Page:",this.props.object);
        this.title = this.props.object['displayName'] + "'s Profile";
        this.state = {posts:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
        GetAuthorRequest.getMe((me)=>{
            GetHisPostsRequest.get(
                ExtractIdFromURL.extract(me.id),
                ExtractIdFromURL.extract(this.props.object['id']) ,
                (PostList)=>{
                    this.setState({posts:PostList.posts.map(
                        (post)=> <PostContainer me={false} key={post['id']} object={post} refresh={this.componentWillMount} />)
                    });
                    if (callback){
                        callback()
                    }
                }
        )
        });

    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title={this.title} iconElementLeft={<div/>}/>
                <ul className="mainList">
                    <li>
                       <ProfileCard object={this.props.object} refresh={this.componentWillMount}/>
                    </li>
                    {this.state.posts}
                </ul>
            </Paper>
        );
    }
}