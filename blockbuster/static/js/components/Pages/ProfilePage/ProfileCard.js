import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
// import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import Divider from 'material-ui/Divider'
import GetRelationshipWithMeRequest from '../../Requests/GetRelationshipWithMeRequest'
import ExtractIdFromURL from '../../Requests/ExtractIdFromURL'
import WithdrawPendingToolbar from '../../SubComponents/RelationshipToolbars/WithdrawPendingToolbar'
import AcceptRejectToolbar from '../../SubComponents/RelationshipToolbars/AcceptRejectToolbar'
import UnFriendToolbar from '../../SubComponents/RelationshipToolbars/UnFriendToolbar'
import BefriendToolbar from '../../SubComponents/RelationshipToolbars/BefriendToolbar'
import UnfollowToolbar from '../../SubComponents/RelationshipToolbars/UnfollowToolbar'
import MyselfToolbar from '../../SubComponents/RelationshipToolbars/MyselfToolbar'

export default class ProfileCard extends React.Component {
    constructor(object, refresh) {
        // props: refresh: callback function to re-render profile page
        super(object, refresh);
        this.getRelationshipWithMe = this.getRelationshipWithMe.bind(this);
        this.changeButton = this.changeButton.bind(this);
        this.afterEditProfile = this.afterEditProfile.bind(this);
        this.state = {
            username: this.props.object['displayName'],
            github: this.props.object['github'] ? this.props.object['github'] : "Don't have one yet",
            bio: this.props.object['bio'] ? this.props.object['bio'] : "Don't have one yet",
            host: this.props.object['host'],
            url: this.props.object['url']
        };
        this.getRelationshipWithMe();
    }

    afterEditProfile(data){
        if (data.id){
            this.setState({
                username: data['displayName'],
                github: data['github'] ? data['github'] : "Don't have one yet",
                bio: data['bio'] ? data['bio'] : "Don't have one yet",
                host: data['host'],
                url: data['url']
            })
        }

    }
    changeButton(res){
        console.log("profile card, object:",this.props.object);
        console.log(res);
        if (res === "The profile with the given UUID is your own."){
            this.setState({button: <MyselfToolbar object={this.props.object} refresh={this.afterEditProfile}/>})
        } else if (res === "No Relationship Found."){
            // send Friend Request Button
            this.setState({button: <BefriendToolbar friend={this.props.object} refresh={this.changeButton}/>})

        } else if (res['status'] === "status_friends"){
            this.setState({button: <UnFriendToolbar object={res} refresh={this.changeButton}/>})

        } else if (res['status'] === "status_friendship_pending"){
            // Cancel Request(not in the requirements) or Reject/Accept Pending request
            if (res['friend']['url'] === this.props.object['url']){
                this.setState({button:<WithdrawPendingToolbar object={res} refresh={this.changeButton}/>})
            } else {
                this.setState({button:<AcceptRejectToolbar object={res} refresh={this.changeButton}/>})
            }

        } else if (res['status'] === "status_following"){
            // UnFollow
            if (res['friend']['url'] === this.props.object['url']){
                // if I am the author
                this.setState({button:<UnfollowToolbar object={res} refresh={this.changeButton}/>})
            } else {
                // if I am the friend
                this.setState({button:<BefriendToolbar friend={this.props.object} refresh={this.changeButton}/>})
            }
            
        }
    }

    getRelationshipWithMe(){
        GetRelationshipWithMeRequest.get(ExtractIdFromURL.extract(this.props.object['id']) ,this.changeButton)
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title={"Username: "+this.state.username}/>
                <Divider/>
                <CardHeader title={"GitHub  : "+this.state.github}/>
                <Divider/>
                <CardHeader title={"Host: "+this.state.host}/>
                <Divider/>
                <CardHeader title={"URL: "+this.state.url}/>
                <Divider/>
                <CardHeader title={"Bio: "+this.state.bio}/>
                <Divider/>
                {this.state.button}
            </Card>
        );
    }
}

ProfileCard.propTypes = {
    // the target author
    object: React.PropTypes.object.isRequired,

    // refresh callback function to re-render profile page
    refresh: React.PropTypes.func.isRequired,
};