import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import GetMyPendingRequest from './GetMyPendingRequest'
import PendingContainer from './PendingContainer'
import SendFollowCard from './SendFollowCard'

export default class MyFriends extends React.Component{
	constructor(object, changePage){
        super(object, changePage);
        console.log(this.props)
        this.state = {pendings:<li/>};
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    componentWillMount(callback){
    	console.log("about to load");
        GetMyPendingRequest.getPending(this.props.object['uuid'],
            (PendingList)=>{
                this.setState({pendings:PendingList.map(
                    (pending, index)=> <PendingContainer key={index++} object={pending} refresh={this.componentWillMount} changePage={this.props.changePage}/>)
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
                        	<h4 style={{color:'#757575', textAlign:'center'}}> Pending Friendship Requests </h4> 
                        </div>
                    	{this.state.pendings}
                </ul>
            </Paper>
        );
    }
}