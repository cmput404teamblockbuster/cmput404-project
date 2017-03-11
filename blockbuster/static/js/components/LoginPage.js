import React from 'react'
import LoginTopBar from './SubComponents/LoginTopBar'
import Paper from 'material-ui/Paper'
import LoginForm from './SubComponents/LoginForm'
import FlatButton from 'material-ui/FlatButton'
export default class LoginPage extends React.Component{
    // props: finishLogIn: call back function to finish login
    render(){
        const styles={
            bodyWrapper:{
                fontSize:'2em',
                  textAlign:'center',
                  color:'gray',
                  width:'100%',
                  height:'100%',
                  position:'fixed',
          },
            p1:{
              color:'white',
            },
            p2:{
                fontSize:'0.5em'
            },
            p3:{

            }
        };
        return(
            <div>
                <LoginTopBar/>
                <Paper style={styles.bodyWrapper}>
                    <p style={styles.p1}>
                        Log in to BlockBuster
                    </p>
                    <LoginForm finishLogin={this.props.finishLogin}/>
                    <p style={styles.p2}>
                        Don't have an account yet?
                    </p>
                    <FlatButton label="Register Here" primary={true}/>
                </Paper>
            </div>
        );
    }
}