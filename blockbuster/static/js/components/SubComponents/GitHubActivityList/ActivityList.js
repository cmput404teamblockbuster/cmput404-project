import React from 'react'
import {Card, CardHeader, CardActions, CardMedia, CardText} from 'material-ui/Card'
import AppBar from 'material-ui/AppBar'
import GetGitHubActivityRequest from '../../Requests/GetGitHubActivityRequest'
import DetermineTheActivity from './DetermineTheActivity'
import FlatButton from 'material-ui/FlatButton'
import Last from 'material-ui/svg-icons/navigation/chevron-left'
import Next from 'material-ui/svg-icons/navigation/chevron-right'
import ListBody from './ListBody'

export default class ActivityList extends React.Component{
    constructor(props){
        super(props);
        this.state = {activities:<CardHeader expandable={true} subtitle="No GitHub Account"/>};
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
                    // if the request sent excess the rate limit
                    this.setState({activities:<CardHeader expandable={true} subtitle="SLOW DOWN BRUH!!!!"/>})
                } else {
                    // convert activities to a list of markdown strings
                    const strings = response.map((activity)=>DetermineTheActivity.getMarkDown(activity.type,activity));
                    this.setState({activities:<ListBody page={this.page} changePage={this.changePage} listOfObjects={strings} actor={response[0].actor}/>})
                }
            } else {
                this.setState({activities:<CardHeader expandable={true} subtitle="No GitHub Account"/>})
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
                <Card containerStyle={this.styles}>
                    <CardHeader actAsExpander={true} showExpandableButton={true} title={"GitHub Activities"}/>
                    <CardMedia expandable={true} mediaStyle={{height:'300px'}}>
                        {this.state.activities}
                    </CardMedia>
                    <CardActions expandable={true}>
                        <FlatButton icon={<Last/>} label="Previous" className="previousButton"/>
                        <span style={{padding:'0 11px 0 11px'}} >{this.page}</span>
                        <FlatButton icon={<Next/>} label="Next" labelPosition='before' className="nextButton"/>
                    </CardActions>
                </Card>
            </div>
        );
    }
}

ActivityList.propTypes = {
    me: React.PropTypes.object.isRequired,
};