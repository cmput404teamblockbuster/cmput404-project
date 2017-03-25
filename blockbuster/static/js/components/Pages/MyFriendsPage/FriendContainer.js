import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import NameLink from '../../SubComponents/PostList/NameLink'
import RespondToPending from './RespondToPending'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import FlatButton from 'material-ui/FlatButton'

export default class FriendContainer extends React.Component{
    constructor(object,refresh){
        super(object,refresh);
        this.showRow = this.showRow.bind(this);
        console.log("Friend Container Object: ");
        console.log(this.props.object);
        this.state = {friend:<li/>};



        //this.friend = undefined;

        var friendId = this.props.object.split("/profile/");
        friendId = friendId[0] + "/api/author/" + friendId[1];
        console.log("Getting Author with id/url: " + friendId);
        GetAuthorRequest.getHim(friendId, this.showRow);

    }

    showRow(friend){
        console.log("Gotten Author Object: ");
        console.log(friend);

        this.setState({friend:<NameLink object={friend}/>});

        return(
            <li>
                <Card className="textField" style={{paddingBottom:'5px'}}>
                    <CardHeader title={<NameLink object={friend}/>}/>
                    HELLO
                </Card>
            </li>
        );


    }



    render(){


        return(
            <div>
            {this.state.friend}
            </div>
        );
    }
}