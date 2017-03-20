import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import ProfileCard from './ProfileCard'
import GetHisPostsRequest from '../../Requests/GetHisPostsRequest'
import PostContainer from '../../SubComponents/PostList/PostContainer'

export default class ProfilePage extends React.Component{
    constructor(object){
        // props: object
        super(object);

    }

    componentWillMount(callback){
        console.log("Profile Page");
        console.log(this.props.object);
        this.title = this.props.object['username'] + "'s Profile";
        this.state = {posts:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
        GetHisPostsRequest.get(this.props.object['uuid'],
            (PostList)=>{
                this.setState({posts:PostList.map(
                    (post)=> <PostContainer key={post['uuid']} object={post} refresh={this.componentWillMount} />)
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
                <AppBar className="title" title={this.title} iconElementLeft={<div/>}/>
                <ul className="mainList">
                    <li>
                       <ProfileCard object={this.props.object}/>
                    </li>
                    {this.state.posts}
                </ul>
            </Paper>
        );
    }
}