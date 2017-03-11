import React from 'react'
import TopBar from './SubComponents/TopBar'
import Drawer from 'material-ui/Drawer'
import MyStream from './SubComponents/MyStream'
import MyFriends from './SubComponents/MyFriends'
import MyProfile from './SubComponents/MyProfile'

export default class BasePage extends React.Component{
    constructor(props){
        // props: checkLogIn: call back function to finish login
        super(props);
        this.state = {currentPage:<MyStream/>};
        this.changePage = this.changePage.bind(this);
    }

    changePage(index){
        console.log(index);
        switch (index){
            case 0:
                this.setState({currentPage:<MyStream/>});
                break;
            case 1:
                this.setState({currentPage:<MyFriends/>});
                break;
            case 2:
                this.setState({currentPage:<MyProfile/>});
                break;
        }

    }

    render(){
        return (
            <div>
                <TopBar change={this.changePage} checkLogin={this.props.checkLogIn}/>
                {this.state.currentPage}
            </div>
        );
    }
}