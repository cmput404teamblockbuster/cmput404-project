import React from 'react'
import TopBar from './SubComponents/TopBar'
import Drawer from 'material-ui/Drawer'
import MyStream from './SubComponents/MyStream'
import MyFriends from './SubComponents/MyFriends'
import ProfilePage from './SubComponents/ProfilePage'
import GetMeRequest from './SubComponents/GetMeRequest'

export default class BasePage extends React.Component{
    constructor(props){
        // props: checkLogIn: call back function to finish login
        super(props);
        this.changePage = this.changePage.bind(this);

        this.state = {currentPage:<MyStream changePage={this.changePage} />};

        GetMeRequest.getAuthor((author)=> {this.author= author;});


    }

    changePage(index,data){
        console.log(index);
        switch (index){
            case 0:
                this.setState({currentPage:<MyStream changePage={this.changePage} />});
                break;
            case 1:
                this.setState({currentPage:<MyFriends changePage={this.changePage}/>});
                break;
            case 2:
                this.setState({currentPage:<ProfilePage changePage={this.changePage} object={this.author}/>});
                break;
            case 3:
                this.setState({currentPage:<ProfilePage changePage={this.changePage} object={data}/>});
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