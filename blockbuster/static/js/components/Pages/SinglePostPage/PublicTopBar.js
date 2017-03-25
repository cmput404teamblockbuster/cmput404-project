import React from 'react';
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';
import RaisedButton from 'material-ui/RaisedButton';


export default class PublicTopBar extends React.Component{
    constructor(){
        super();

        this.Login = this.Login.bind(this);
    }


    Login(){
        const path = "/login/";
        window.location.assign(path);
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
                    <RaisedButton label="Login" style={styles.button} onTouchTap={this.Login}/>
                </ToolbarGroup>
            </Toolbar>

        );
    }
}