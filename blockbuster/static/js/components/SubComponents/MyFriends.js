import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'
import MakePost from './MakePost'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import TextField from 'material-ui/TextField'
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar'
import FlatButton from 'material-ui/FlatButton'
import {Table, TableBody, TableHeader, TableHeaderColumn, TableRow, TableRowColumn}
  from 'material-ui/Table';
import ChangeRelationRequest from './ChangeRelationRequest'

const tableData = [
  {
    name: 'John Smith',
    status: 'Employed',
  },
  {
    name: 'Randal White',
    status: 'Unemployed',
  },
  {
    name: 'Stephanie Sanders',
    status: 'Employed',
  },
];


export default class MyFriends extends React.Component{

	constructor(props) {
    	super(props);
    	this.handleTextChange = this.handleTextChange.bind(this);
        this.handleFollow = this.handleFollow.bind(this);
        this.handleUnFriend = this.handleUnFriend.bind(this);

        this.data = {receiver:"", status:"status_friendship_pending"};
	}
    
    handleFollow(){
        alert("Attempting to follow username:" + this.data.receiver);
         if (this.data.receiver !== ""){
         	//this.requestStatus = {};
         	//this.requestStatus["status"] = 'status_pending';
            ChangeRelationRequest.send(this.data.receiver, this.data.status);
        }
       
    }
    handleTextChange(event){
        this.data.receiver = event.target.value;

    }

    handleUnFriend(index){
        //alert("Attempting to stop following" + index);
       
    }

    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="My Friends" iconElementLeft={<div/>}/>
					<Paper style={{backgroundColor: '#424242', padding:'10px 20px 10px 20px', margin: '10px 20px 10px 20px'}} zDepth={1}>
						<p className="innerText"> Follow this author: </p>
	                	<TextField hintStyle={{paddingLeft:'20px'}} 
	                		textareaStyle={{padding:'0px 20px 0px 20px'}} onChange={this.handleTextChange} hintText="Author's UUID"/>
	                	<FlatButton style={{marginLeft: '20px'}} label="Follow" onTouchTap={this.handleFollow}/>
	                	<p className="innerText"> If the author follows you back you will become friends! </p>
	                </Paper>     
	                <div>
	                	        	<Table height={'250px'} selectable={false} multiSelectable={false} >
        		<TableHeader displaySelectAll={false}>
        			<TableRow>
        					
	        			<TableHeaderColumn colSpan="3" style={{textAlign: 'center', color:'#9E9E9E'}}>
	        				Friends
	        			</TableHeaderColumn>
        			</TableRow>
        		</TableHeader>
        		<TableBody displayRowCheckbox={false}>
					{tableData.map( (row, index) => (
						<TableRow key={index} selected={row.selected}>
						    <TableRowColumn>{row.name}</TableRowColumn>
						    <TableRowColumn>{row.status}</TableRowColumn>
						    <TableRowColumn>
						        <FlatButton style={{float: 'right' }} label="Remove" onTouchTap={this.handleUnFriend(index)}/>
						    </TableRowColumn>
						    </TableRow>
						    ))}
				</TableBody>
        	</Table>
	                </div>   
            </Paper>
        );
    }
}