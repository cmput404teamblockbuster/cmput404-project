import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import GetGitHubActivityRequest from '../../Requests/GetGitHubActivityRequest'
import PostContainer from '../../SubComponents/PostList/PostContainer'
export default class ActivityList extends React.Component{
    constructor(){
        super();
        this.state = {posts:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
        this.gitHub = this.props.me.github;
        GetGitHubActivityRequest.get(this.gitHub,()=>{})

    }


    render(){
        return(
            <div className="GitHubList">
                <AppBar className="title" title="GitHub Activity" iconElementLeft={<div/>}/>
                <ul className="mainList">
                    <li>
                    </li>
                    {this.state.posts}
                </ul>
            </div>
        );
    }
}

ActivityList.propTypes = {
    me: React.PropTypes.object
}