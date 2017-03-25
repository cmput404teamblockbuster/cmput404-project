import React from 'react'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import {List, ListItem} from 'material-ui/List';
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import SearchListItem from './SearchListItem'

export default class SearchUserDialog extends React.Component{
    constructor(open,closeAction, changePage){
        super(open, closeAction, changePage);

        this.getAllUsers = this.getAllUsers.bind(this);
        // this.goToProfile = this.goToProfile.bind(this);

        this.state = {items:null};

        this.getAllUsers();
    }


    getAllUsers(){
        const cb= (objectList) =>{
            this.setState({items: objectList.results.map(
                (object)=><SearchListItem key={object['id']} object={object} changePage={this.props.changePage}/>
            )})
        };

        GetAuthorRequest.getAll(cb)
    }

    render(){
        const actions=[
            <FlatButton label="Close" onTouchTap={this.props.closeAction}/>
        ];
        return(
            <Dialog open={this.props.open} actions={actions} autoScrollBodyContent={true}>
                <List>
                    {this.state.items}
                </List>
            </Dialog>
        );
    }
}