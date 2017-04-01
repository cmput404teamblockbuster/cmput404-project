import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import EditProfileDialog from './EditProfileDialog';

export default class MyselfToolbar extends React.Component{
    constructor(props){
        super(props);

        this.handleEdit = this.handleEdit.bind(this);
        this.closeDialog = this.closeDialog.bind(this);
        this.state = {dialog:false, object:this.props.object};
    }

    closeDialog(data){
        if(data.id){
            this.setState({object:data, dialog:false})
        } else{
            this.setState({dialog:false})
        }

    }

    handleEdit(){
        this.setState({dialog:<EditProfileDialog refresh={this.props.refresh} closeAction={this.closeDialog} object={this.state.object}/>})
    }

    render(){
        return(
            <Toolbar style={{backgroundColor:'#424242', border:'solid 1px #4FC3F7'}} >
                <ToolbarGroup>
                </ToolbarGroup>
                <ToolbarGroup>
                    <RaisedButton label="Edit My Profile" onTouchTap={this.handleEdit}/>
                </ToolbarGroup>
                <ToolbarGroup>
                </ToolbarGroup>
                {this.state.dialog}
            </Toolbar>
        );
    }
}

MyselfToolbar.propTypes = {
    // myself as the object
    object: React.PropTypes.object.isRequired,

    refresh: React.PropTypes.func.isRequired,
};