import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';

export default class MyselfToolbar extends React.Component{
    constructor(props){
        super(props);

        this.handleEdit = this.handleEdit.bind(this);
    }

    handleEdit(){
        alert("TODO: edit profile")
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
            </Toolbar>
        );
    }
}

MyselfToolbar.propTypes = {
    // myself as the object
    object: React.PropTypes.object.isRequired,

    refresh: React.PropTypes.func.isRequired,
};