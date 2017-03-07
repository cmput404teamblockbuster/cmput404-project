import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from './components/AppWrapper'
import BasePage from './components/BasePage'
import LoginPage from './components/LoginPage'


class Main extends React.Component{
    constructor(props){
        super(props);
        this.state = {loggedIn:false, page:<LoginPage/>};

        this.checkLogIn = this.checkLogIn.bind(this);
        this.componentWillMount = this.componentWillMount.bind(this);
    }

    checkLogIn(){
        //todo check log in function

        // if success:
        this.setState({loggedIn:true, page:<BasePage/>});

        // if faile:
        // this.setState({loggedIn:false,page:<LoginPage/>});
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