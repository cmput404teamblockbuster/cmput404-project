import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from './components/AppWrapper'
import BasePage from './components/BasePage'
import LoginPage from './components/LoginPage'
import auth from './components/SubComponents/auth'

class Main extends React.Component{
    constructor(props){
        super(props);
        this.state = {loggedIn:false, page:<LoginPage/>};

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
            this.setState({loggedIn:true, page:<BasePage checkLogIn={this.checkLogIn}/>});
        } else {
            // if faile:
            this.setState({loggedIn:false,page:<LoginPage finishLogin={this.finishLogin} />});
        }


    }

    componentWillMount(){
        this.checkLogIn();
    }


    render() {
        return (
            <AppWrapper>
                {this.state.page}
            </AppWrapper>
        );
    }
}

ReactDom.render(<Main />,
document.getElementById('container'));