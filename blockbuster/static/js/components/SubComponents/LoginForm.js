import React from 'react'
import TextField from 'material-ui/TextField'
import {Card,CardMedia,CardActions } from 'material-ui/Card'
import RaisedButton from 'material-ui/RaisedButton'
export default class LoginForm extends React.Component{
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
                    <TextField hintText="Username" />
                    <TextField hintText="Password"  type="password"/>
                </CardMedia>
                <CardActions>
                    <RaisedButton label="Login" labelStyle={styles.button}/>
                </CardActions>
            </Card>
        );
    }
}