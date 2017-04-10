import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import GetSinglePostRequest from '../../Requests/GetSinglePostRequest'
import ExtractIdFromURL from '../../Requests/ExtractIdFromURL'
import PostContainer from '../../SubComponents/PostList/PostContainer'
import EmptyPost from './EmptyPost'

export default class SinglePostPage extends React.Component{
    constructor(object){
        // props: object
        super(object);
        this.state = {post:<EmptyPost/>}
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
        const uuid = ExtractIdFromURL.extract(window.location.pathname) ;
        if (uuid){
            GetSinglePostRequest.get(uuid,(res)=>{
                    this.setState({post: res? <PostContainer single={true} object={res} refresh={this.componentWillMount}/> :<EmptyPost/>});
                    if (callback){
                        callback();
                    }
            })
        }
    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="A Post" iconElementLeft={<div/>}/>
                <ul className="mainList">
                    {this.state.post}
                </ul>
            </Paper>
        );
    }
}