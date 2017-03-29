import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField'
import GetSinglePostRequest from '../../Requests/GetSinglePostRequest'

export default class EditProfileDialog extends React.Component{
    constructor(props){
        super(props);

        this.handleClose = this.handleClose.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.changeGithub = this.changeGithub.bind(this);
        this.changeBio = this.changeBio.bind(this);

        if (this.props.object.github){
            this.github = this.props.object.github
        }
        if (this.props.object.bio){
            this.bio = this.props.object.bio
        }
        this.actions = [
            <FlatButton label="Cancel" onTouchTap={this.handleClose}/>,
            <FlatButton label="Submit" onTouchTap={this.handleSubmit}/>
        ];
        this.author = undefined;
    }

    changeGithub(event){
        this.data.github = event.target.value;
    }

    changeBio(event){
        this.data.bio = event.target.value
    }

    handleClose(){
        this.props.refresh();
        this.props.closeAction();
    }

    handleSubmit(){

    }

    render(){
        return(
            <Dialog open={true} actions={this.actions} title="Edit Profile" autoScrollBodyContent={true}>
                <TextField floatingLabelText="GitHub" value={this.github} fullWidth={true} onChange={this.changeGithub}/>
                <br/>
                <TextField floatingLabelText="Bio" value={this.bio} fullWidth={true} multiLine={true} onChange={this.changeBio}/>
            </Dialog>
        )}

}

EditProfileDialog.propTypes = {

    refresh: React.PropTypes.func.isRequired,

    closeAction: React.PropTypes.func.isRequired,
    // the user object
    object: React.PropTypes.object.isRequired,
};