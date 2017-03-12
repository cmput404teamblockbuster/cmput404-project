import React from 'react'
import Dialog from 'material-ui/Dialog'
import FlatButton from 'material-ui/FlatButton'
import TextField from 'material-ui/TextField'
import CreateUserReuqest from './CreateUserReuqest'


export default class RegistrationDialog extends React.Component{

    constructor(open, closeAction){
        // props: {open: boolen determin if this dialog is open
        //         closeAction: callabck function to close the dialog}
        super(open, closeAction);
        this.cancel = this.cancel.bind(this);
        this.submit = this.submit.bind(this);
        this.nameChange = this.nameChange.bind(this);
        this.emailChange = this.emailChange.bind(this);
        this.passChange = this.passChange.bind(this);
        this.matchChange = this.matchChange.bind(this);

        this.requiredText = "This Field is required";
        this.notMatchText = "Password does not match";

        this.state = {username:"", pass:"", email:"", nameError:this.requiredText, emailError:this.requiredText, passError:this.requiredText, matchError:this.requiredText};
        this.actions = [
            <FlatButton label="Cancel" primary={true} onTouchTap={this.cancel}/>,
            <FlatButton label="Submit" primary={true} onTouchTap={this.submit}/>]
    }


    nameChange(event){
        if (event.target.value !== ""){
            this.setState({username:event.target.value, nameError:""})
        } else {
            this.setState({username:event.target.value, nameError:this.requiredText})
        }
    }

    emailChange(event){
        if (event.target.value !== ""){
            this.setState({email:event.target.value, emailError:""})
        } else {
            this.setState({email:event.target.value, emailError:this.requiredText})
        }
    }

    passChange(event){
        if (event.target.value !== ""){
            this.setState({pass:event.target.value, passError:""})
        } else {
            this.setState({pass:event.target.value, passError:this.requiredText})
        }
    }

    matchChange(event){
        if (event.target.value !== ""){
            if (event.target.value !== this.state.pass){
                this.setState({matchError:this.notMatchText})
            } else {
                this.setState({matchError:""})
            }
        } else {
            this.setState({matchError:this.notMatchText})
        }
    }

    cancel(){
        this.props.closeAction();
    }

    submit(){
        if (this.state.username!=="" &&
            this.state.pass!=="" &&
            this.state.email!=="" &&
            this.state.matchError==""){
            CreateUserReuqest.send(this.state.username, this.state.pass, this.state.email, this.cancel)
        }
    }

    render(){
        return (
            <Dialog
                open={this.props.open}
                title="Registration"
                actions={this.actions}
                onRequestClose={this.cancel}
                autoScrollBodyContent={true}
                contentStyle={{width:'30%'}}
            >
                <TextField floatingLabelText="Username" fullWidth={true} onChange={this.nameChange} errorText={this.state.nameError}/> <br/>
                <TextField floatingLabelText="Email" fullWidth={true} onChange={this.emailChange} errorText={this.state.emailError}/> <br/>
                <TextField floatingLabelText="Password" fullWidth={true} onChange={this.passChange} errorText={this.state.passError} type='password'/> <br/>
                <TextField floatingLabelText="Confirm Password" fullWidth={true} onChange={this.matchChange} errorText={this.state.matchError} type='password'/>
            </Dialog>
        );
    }
}