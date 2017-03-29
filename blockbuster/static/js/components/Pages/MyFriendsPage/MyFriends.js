import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import Divider from 'material-ui/Divider'
import GetMyPendingRequest from '../../Requests/GetMyPendingRequest'
import GetMyRelationshipsRequest from '../../Requests/GetMyRelationshipsRequest'
import PendingContainer from './PendingContainer'
import ListItemContainer from './ListItemContainer'


export default class MyFriends extends React.Component{
	constructor(object){
        super(object);
        this.state = {pendings:<li/>, friends:<li/>,  followings:<li/>, followers:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
    	console.log("about to load");
        GetMyPendingRequest.getPending(this.props.object['id'],
            (PendingList)=>{
                this.setState({pendings:PendingList.map(
                    (pending, index)=> <PendingContainer key={index++} object={pending} refresh={this.componentWillMount}/>)
                });
                if (callback){
                    callback()
                }
            }
        );
        GetMyRelationshipsRequest.getFriends(
            (friendsList)=>{
                this.setState({friends:friendsList.results.map(
                    (friend,index)=> <ListItemContainer key={index} object={friend} status="friends" refresh={this.componentWillMount} />
                )})
            }
        );
        GetMyRelationshipsRequest.getFollowers(
            (followerList)=>{
                this.setState({followers: followerList.map(
                    (follower,index)=> <ListItemContainer key={index} object={follower} status="follower" refresh={this.componentWillMount}/>
                )})
            }
        );
        GetMyRelationshipsRequest.getFollowings(
            (followingList)=>{
                this.setState({followings: followingList.map(
                    (following,index)=> <ListItemContainer key={index} object={following} status="following" refresh={this.componentWillMount}/>
                )})
            }
        )

    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Friends" iconElementLeft={<div/>}/>
                <ul className="mainList">
                    {/*<li>*/}
                        {/*<SendFollowCard object={this.props.object}/>*/}
                    {/*</li>*/}


                    <Divider/>
                    <div>
                        <h4 id="pendingHeader"> Received Friendship Requests </h4>
                    </div>
                    {this.state.pendings}

                    <Divider/>
                    <div>
                        <h4 id="pendingHeader"> My Friends</h4>
                    </div>
                    {/*<MyFriendsTable object={this.props.object} refresh={this.props.refresh}/>*/}
                    {this.state.friends}

                    <Divider/>
                    <div>
                        <h4 id="pendingHeader"> Users I Follow </h4>
                    </div>
                    {this.state.followings}

                    <Divider/>
                    <div>
                        <h4 id="pendingHeader"> My Followers </h4>
                    </div>
                    {this.state.followers}
                    <Divider/>

                </ul>
            </Paper>
        );
    }
}