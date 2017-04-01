import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField'
import PutProfileRequest from '../../Requests/PutProfileRequest'
import ExtractIdFromURL from '../../Requests/ExtractIdFromURL'

export default class EditProfileDialog extends React.Component{
    constructor(props){
        super(props);

        this.handleClose = this.handleClose.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.changeGithub = this.changeGithub.bind(this);
        this.changeBio = this.changeBio.bind(this);

        this.state = {github:this.props.object.github, bio:this.props.object.bio};
        this.actions = [
            <FlatButton label="Cancel" onTouchTap={this.handleClose}/>,
            <FlatButton label="Submit" onTouchTap={this.handleSubmit}/>
        ];
        this.author = undefined;
    }

    changeGithub(event){
        this.setState({github: event.target.value});
    }

    changeBio(event){
        this.setState({bio:event.target.value})
    }

    handleClose(data){
        this.props.refresh(data);
        this.props.closeAction(data);
    }

    handleSubmit(){
        const cb = (data)=>{
            this.handleClose(data);
        };


        PutProfileRequest.put(this.state.github,this.state.bio,ExtractIdFromURL.extract(this.props.object.id),cb)
    }

    render(){
        return(
            <Dialog open={true} actions={this.actions} title="Edit Profile" autoScrollBodyContent={true}>
                <TextField floatingLabelText="GitHub" value={this.state.github} fullWidth={true} onChange={this.changeGithub}/>
                <br/>
                <TextField floatingLabelText="Bio" value={this.state.bio} fullWidth={true} multiLine={true} onChange={this.changeBio}/>
            </Dialog>
        )}

}

EditProfileDialog.propTypes = {

    refresh: React.PropTypes.func.isRequired,

    closeAction: React.PropTypes.func.isRequired,
    // the user object
    object: React.PropTypes.object.isRequired,
};