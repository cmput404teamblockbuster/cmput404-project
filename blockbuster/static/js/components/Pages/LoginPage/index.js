import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import LoginPage from './LoginPage'
import auth from '../../Requests/auth'

class Main extends React.Component{
    constructor(props){
        super(props);

        this.checkLogIn = this.checkLogIn.bind(this);
        this.finishLogin = this.finishLogin.bind(this);
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    finishLogin(){
        this.checkLogIn()
    }

    checkLogIn(){
        if(auth.loggedIn()){
            // if success:
            if(document.referrer){
                // back to where you come from
                window.history.go(-1);
            } else {
                // go to home page
                window.location.assign("/");
            }

        }
    }

    componentWillMount(){
        this.checkLogIn();
    }


    render() {
        return (
            <AppWrapper loginPage={true}>
                <LoginPage finishLogin={this.finishLogin} />
            </AppWrapper>
        );
    }
}

ReactDom.render(<Main />,
document.getElementById('container'));