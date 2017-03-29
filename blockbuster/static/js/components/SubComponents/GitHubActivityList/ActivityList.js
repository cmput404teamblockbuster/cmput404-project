import React from 'react'
import {Card, CardHeader, CardActions, CardMedia} from 'material-ui/Card'
import AppBar from 'material-ui/AppBar'
import GetGitHubActivityRequest from '../../Requests/GetGitHubActivityRequest'
import PostContainer from '../../SubComponents/PostList/PostContainer'
export default class ActivityList extends React.Component{
    constructor(){
        super();
        this.state = {activities:<li/>};
        this.gitHub = this.props.me.github;
        this.page = 1;

        this.getData = this.getData.bind(this);
        this.changePage = this.changePage.bind(this);

        this.getData(1)
    }

    getData(page){
        GetGitHubActivityRequest.get(this.gitHub,page,(response)=>{
            if (response){
                if (response==="Try Again Later"){

                } else {

                }
            }
        })
    }

    changePage(up){
        this.page = up? this.page+1 : this.page-1;
        if (this.page === 0){
            this.page = 1;
        }
        this.getData(this.page);

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
    me: React.PropTypes.object.isRequired,
};