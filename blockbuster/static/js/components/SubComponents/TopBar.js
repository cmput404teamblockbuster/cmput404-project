import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';
import SearchIcon from 'material-ui/svg-icons/action/search';
import TextField from 'material-ui/TextField'

export default class TopBar extends React.Component{
    constructor(change){
        // change is a function that will change the page
        super(change);
        this.Stream = this.Stream.bind(this);
        this.Friends = this.Friends.bind(this);
        this.Profile = this.Profile.bind(this);
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
                    <RaisedButton label="My Stream" style={styles.button} onTouchTap={this.Stream}/>
                    <RaisedButton label="My Friends" style={styles.button} onTouchTap={this.Friends}/>
                    <RaisedButton label="My Profile" style={styles.button} onTouchTap={this.Profile}/>
                    <RaisedButton label="Logout" style={styles.button}/>
                </ToolbarGroup>
            </Toolbar>

        );
    }
}