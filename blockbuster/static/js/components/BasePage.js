import React from 'react'
import TopBar from './SubComponents/TopBar'
import Drawer from 'material-ui/Drawer'
import MyStream from './Pages/MyStreamPage/MyStream'
import MyFriends from './Pages/MyFriendsPage/MyFriends'
import ProfilePage from './Pages/ProfilePage/ProfilePage'
import ProfilePage2 from './Pages/ProfilePage/ProfilePage2'
import GetMeRequest from './Requests/GetMeRequest'

export default class BasePage extends React.Component{
    constructor(props){
        // props: checkLogIn: call back function to finish login
        super(props);
        this.changePage = this.changePage.bind(this);

        this.state = {currentPage:<MyStream changePage={this.changePage} />, count:0};

        GetMeRequest.getAuthor((author)=> {this.author= author;});


    }

    changePage(index,data){
        console.log(index);
        this.setState({count:this.state.count+1})
        switch (index){
            case 0:
                this.setState({currentPage:<MyStream changePage={this.changePage} />});
                break;
            case 1:
                this.setState({currentPage:<MyFriends changePage={this.changePage} object={this.author}/>});;
                break;
            case 2:
                if (this.state.count % 2 === 0){
                    this.setState({currentPage:<ProfilePage2 changePage={this.changePage} object={this.author}/>});
                } else {
                    this.setState({currentPage:<ProfilePage changePage={this.changePage} object={this.author}/>});
                }

                break;
            case 3:
                // to let react notice that this state actually changed, otherwist it won't notice any change if the prop changes
                if(this.state.count % 2 === 0){
                    this.setState({currentPage:<ProfilePage2 changePage={this.changePage} object={data} count={this.state.count}/>});
                } else{
                    this.setState({currentPage:<ProfilePage changePage={this.changePage} object={data} count={this.state.count}/>});
                }

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