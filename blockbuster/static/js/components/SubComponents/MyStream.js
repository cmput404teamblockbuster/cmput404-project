import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import MakePost from './MakePost'
import GetStreamRequest from './GetStreamRequest'
import PostContainer from './PostContainer'
export default class MyStream extends React.Component{
    constructor(props){
        super(props);
        this.state = {posts:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
        GetStreamRequest.get(
            (PostList)=>{
                console.log(PostList)
                console.log("see here")
                this.setState({posts:PostList.map(
                    (post)=> <PostContainer key={post['uuid']} object={post} refresh={this.componentWillMount}/>)
                })
                if (callback){
                    callback()
                }
            }
        )
    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Stream" iconElementLeft={<div/>}/>
                <ul className="mainList">
                    <li>
                       <MakePost refresh={this.componentWillMount}/>
                    </li>
                    {this.state.posts}
                </ul>
            </Paper>
        );
    }
}