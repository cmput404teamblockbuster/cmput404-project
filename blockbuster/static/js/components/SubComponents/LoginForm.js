import React from 'react'
import TextField from 'material-ui/TextField'
import {Card,CardMedia,CardActions } from 'material-ui/Card'
import RaisedButton from 'material-ui/RaisedButton'
import auth from './auth'

export default class LoginForm extends React.Component{
    constructor(props){
        // props: finishLogin: call back function to finish login
        super(props);
        this.state = {username:'', password:''};

        this.username = this.username.bind(this);
        this.password = this.password.bind(this);
        this.login = this.login.bind(this);
    }

    username(event){
        this.setState({username:event.target.value})
    }

    password(event){
        this.setState({password:event.target.value})
    }

    login(){
        auth.login(this.state.username,this.state.password,(success)=>{
            if (success){
                console.log(localStorage.token)
                this.props.finishLogin()
            }
        })
    }

    render(){
        const styles={
            wrapper:{
                marginLeft: '40%',
                marginRight: '40%',
                padding: '0.2em 0.5em 0.5em 0.5em'
            },
            button:{
              marginBottom: '0 0 1em 0'
            }
        };
        return(
            <Card style={styles.wrapper}>
                <CardMedia>
                    <TextField id='username' hintText="Username" onChange={this.username}/>
                    <TextField id='password' hintText="Password"  type="password" onChange={this.password}/>
                </CardMedia>
                <CardActions>
                    <RaisedButton label="Login" labelStyle={styles.button} onTouchTap={this.login}/>
                </CardActions>
            </Card>
        );
    }
}