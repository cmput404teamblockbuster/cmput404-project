import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import NameLink from '../../SubComponents/PostList/NameLink'
import RespondToPending from './RespondToPending'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import FlatButton from 'material-ui/FlatButton'
import {TableRow, TableRowColumn} from 'material-ui/Table'
import UnFriendToolbar from '../../SubComponents/RelationshipToolbars/UnFriendToolbar'

export default class FriendContainer extends React.Component{
    constructor(object,refresh){
        super(object,refresh);
        this.showRow = this.showRow.bind(this);
        console.log("Friend Container Object: ");
        console.log(this.props.object);
        this.state = {friend:<li/>,button:<li/>};

        var friendId = this.props.object.split("/profile/");
        friendId = friendId[0] + "/api/author/" + friendId[1];
        console.log("Getting Author with url: " + friendId);
        GetAuthorRequest.getHim(friendId, this.showRow);

    }

    showRow(friend){
        console.log("Gotten Author Object: ");
        console.log(friend);

        this.setState({friend:<NameLink object={friend}/>});
        this.setState({button:<UnFriendToolbar object={friend} refresh={this.props.refresh}/>});

    }



    render(){


        return(
            <TableRow key={this.props.key}>
            <TableRowColumn>{this.state.friend}</TableRowColumn>
            <TableRowColumn>{this.state.button}</TableRowColumn>
            </TableRow>
        );
    }
}