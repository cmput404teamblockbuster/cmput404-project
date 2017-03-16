import React from 'react';
import auth from '../Requests/auth'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import darkBaseTheme from 'material-ui/styles/baseThemes/darkBaseTheme'
import injectTapEventPlugin from 'react-tap-event-plugin';
// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();
const muiTheme = getMuiTheme(darkBaseTheme);
// const muiTheme = getMuiTheme();

export default class AppWrapper extends React.Component{

    render(){
        if (! this.props.loginPage){
            auth.checkLogin();
        }
        return (
        <MuiThemeProvider muiTheme={muiTheme}>
            <div>
                {this.props.children}
            </div>
        </MuiThemeProvider>
        );

    }
}