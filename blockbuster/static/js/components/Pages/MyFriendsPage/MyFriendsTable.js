import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import GetMyPendingRequest from '../../Requests/GetMyPendingRequest'
import GetTheirFriendsRequest from '../../Requests/GetTheirFriendsRequest'
import FriendContainer from './FriendContainer'
import SendFollowCard from './SendFollowCard'

export default class MyFriendsTable extends React.Component{
	constructor(object){
        super(object);
        this.state = {friends:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
    	console.log("attempting to load freinds table with object: ");
             console.log(this.props.object);
        GetTheirFriendsRequest.get(this.props.object['id'],
            (FriendsList)=>{
                this.setState({friends:FriendsList.authors.map(
                    (friend, index)=> <FriendContainer key={index++} object={friend} refresh={this.componentWillMount}/>)
                });
                if (callback){
                    callback()
                }
            }
        )
    }


    render(){
        return(
            <Paper className="streamContainer">
                    	<div>
                        	<h4 id="friendsHeader" style={{color:'#757575', textAlign:'center'}}> Your Friends Go Here: </h4>
                        </div>
                    	{this.state.friends}
            </Paper>
        );
    }
}