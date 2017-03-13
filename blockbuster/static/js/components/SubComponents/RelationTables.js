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
import CreatePostRequest from './CreatePostRequest'


const tableData = [
  {
    name: 'John Smith',
    status: 'Employed',
    selected: true,
  },
  {
    name: 'Randal White',
    status: 'Unemployed',
  },
  {
    name: 'Stephanie Sanders',
    status: 'Employed',
    selected: true,
  },
  {
    name: 'Steve Brown',
    status: 'Employed',
  },
  {
    name: 'Joyce Whitten',
    status: 'Employed',
  },
  {
    name: 'Samuel Roberts',
    status: 'Employed',
  },
  {
    name: 'Adam Moore',
    status: 'Employed',
  },
];


export default class RelationTables extends React.Component {
    constructor(props) {
        super(props);
        this.handleUnFriend = this.handleUnFriend.bind(this);
    }

    handleUnFriend(index){
        alert("Attempting to stop following" + index);
       
    }

    render(){
        return(
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
						        <FlatButton style={{float: 'right' }} label="Remove" onClick={this.handleUnFriend(index)}/>
						    </TableRowColumn>
						    </TableRow>
						    ))}
				</TableBody>
        	</Table>
        );
    }
}