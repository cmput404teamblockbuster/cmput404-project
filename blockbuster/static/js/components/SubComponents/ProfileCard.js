import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
// import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import Divider from 'material-ui/Divider'
import GetRelationshipWithMeRequest from './GetRelationshipWithMeRequest'
import WithdrawPendingToolbar from './RelationshipToolbars/WithdrawPendingToolbar'
import AcceptRejcetToolbar from './RelationshipToolbars/AcceptRejcetToolbar'
import UnFriendToolbar from './RelationshipToolbars/UnFriendToolbar'
import BefriendToolbar from './RelationshipToolbars/BefriendToolbar'
import UnfollowToolbar from './RelationshipToolbars/UnfollowToolbar'

export default class ProfileCard extends React.Component {
    constructor(object) {
        // props: refresh: callback function to re-render MyStream
        super(object);
        this.getRelationshipWithMe = this.getRelationshipWithMe.bind(this);
        this.changeButton = this.changeButton.bind(this);

        this.state = {username:this.props.object['username'],
            github:this.props.object['github'] ? this.props.object['github'] : "Don't have one yet" ,
            uuid: this.props.object['uuid'], button:<div/>};
        this.getRelationshipWithMe();
    }

    changeButton(res){
        console.log("profile card");
        console.log(res);
        if (res === "The profile with the given UUID is your own."){
            // your own
        } else if (res === "No Relationship Found."){
            // send Friend Request Button
            this.setState({button: <BefriendToolbar receiver={this.props.object} refresh={this.changeButton}/>})

        } else if (res['status'] === "status_friends"){
            this.setState({button: <UnFriendToolbar object={res}/>})

        } else if (res['status'] === "status_friendship_pending"){
            // Cancel Request(not in the requirements) or Reject/Accept Pending request
            if (res['receiver']['username'] === this.props.object['username']){
                this.setState({button:<WithdrawPendingToolbar object={res}/>})
            } else {
                this.setState({button:<AcceptRejcetToolbar object={res}/>})
            }

        } else if (res['status'] === "status_following"){
            // UnFollow
            this.setState({button:UnfollowToolbar})
        }
    }

    getRelationshipWithMe(){
        GetRelationshipWithMeRequest.get(this.props.object['uuid'],this.changeButton)
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title={"Username: "+this.state.username}/>
                <Divider/>
                <CardHeader title={"Github  : "+this.state.github}/>
                <Divider/>
                <CardHeader title={"UUID: "+this.state.uuid}/>
                <Divider/>
                {this.state.button}
            </Card>
        );
    }
}