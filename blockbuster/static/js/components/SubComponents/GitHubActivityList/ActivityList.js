import React from 'react'
import {Card, CardHeader, CardActions, CardMedia, CardText} from 'material-ui/Card'
import AppBar from 'material-ui/AppBar'
import GetGitHubActivityRequest from '../../Requests/GetGitHubActivityRequest'

export default class ActivityList extends React.Component{
    constructor(props){
        super(props);
        this.state = {activities:<li/>};
        this.gitHub = this.props.me.github;
        this.page = 1;

        this.getData = this.getData.bind(this);
        this.changePage = this.changePage.bind(this);

        this.getData(1)
    }

    getData(page){
        if (this.gitHub){
            GetGitHubActivityRequest.get(this.gitHub,page,(response)=>{
            if (response){
                console.log(response, "in activity list")
                if (response==="Try Again Later"){

                } else {

                }
            } else {
                this.setState
            }
            })
        }

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
                <Card>
                    <CardHeader actAsExpander={true} showExpandableButton={true} title={"GitHub Activities"}/>
                    <CardHeader expandable={true} title="title??"/>
                    <CardText expandable={true}>this is text</CardText>
                </Card>
            </div>
        );
    }
}

ActivityList.propTypes = {
    me: React.PropTypes.object.isRequired,
};