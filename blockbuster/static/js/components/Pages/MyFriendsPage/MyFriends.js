import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import GetMyPendingRequest from '../../Requests/GetMyPendingRequest'
import PendingContainer from './PendingContainer'
import SendFollowCard from './SendFollowCard'
import MyFriendsTable from './MyFriendsTable'

export default class MyFriends extends React.Component{
	constructor(object){
        super(object);
        this.state = {pendings:<li/>};
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
        )
    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Friends" iconElementLeft={<div/>}/>
                	<ul className="mainList">
                    	<li>
                       		<SendFollowCard object={this.props.object}/>
                    	</li>
                    	<div>
                        	<h4 id="pendingHeader" style={{color:'#757575', textAlign:'center'}}> Received Friendship Requests Go Here: </h4>
                        </div>
                    	{this.state.pendings}

                        <MyFriendsTable object={this.props.object} refresh={this.props.refresh}/>

                </ul>
            </Paper>
        );
    }
}