import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import SearchIcon from 'material-ui/svg-icons/action/search';
import TextField from 'material-ui/TextField'
import auth from './auth';
import SearchUserDialog from './SearchUserDialog';
export default class TopBar extends React.Component{
    constructor(change, checkLogin){
        // change is a function that will change the page
        // checkLogin: call back function to finish login
        super(change, checkLogin);

        this.state = { dialog:<div/>};
        this.Stream = this.Stream.bind(this);
        this.Friends = this.Friends.bind(this);
        this.Profile = this.Profile.bind(this);
        this.Logout = this.Logout.bind(this);
        this.OpenSearch = this.OpenSearch.bind(this);
        this.CloseSearch = this.CloseSearch.bind(this);
        this.changePage = this.changePage.bind(this);
    }

    Stream(){
        this.props.change(0)
    }

    Friends(){
        this.props.change(1)
    }
    Profile(){
        this.props.change(2)
    }

    Logout(){
        auth.logout();
        this.props.checkLogin()
    }

    changePage(index, object){
        this.CloseSearch();
        this.props.change(index,object);
    }

    CloseSearch(){
        this.setState({dialog:<SearchUserDialog open={false} closeAction={this.CloseSearch} changePage={this.changePage}/>})
    }

    OpenSearch() {
        this.setState({dialog: <SearchUserDialog open={true} closeAction={this.CloseSearch} changePage={this.changePage}/>})
    }




    render(){
        const styles = {
            black:{
                backgroundColor:'black'
            },
            title: {
                color: 'white',
                fontSize: '150%'
            },
            button:{
                margin:'0.3em'
            }

        };
        return (
            <Toolbar style={styles.black}>
                <ToolbarGroup>
                    <ToolbarTitle text="BlockBuster" style={styles.title}/>
                </ToolbarGroup>
                <ToolbarGroup>
                    {this.state.dialog}
                    <RaisedButton icon={<SearchIcon/>} label="Search People" style={styles.button} onTouchTap={this.OpenSearch}/>
                    <RaisedButton label="My Stream" style={styles.button} onTouchTap={this.Stream}/>
                    <RaisedButton label="My Friends" style={styles.button} onTouchTap={this.Friends}/>
                    <RaisedButton label="My Profile" style={styles.button} onTouchTap={this.Profile}/>
                    <RaisedButton label="Logout" style={styles.button} onTouchTap={this.Logout}/>
                </ToolbarGroup>
            </Toolbar>

        );
    }
}