import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import ProfilePage from './ProfilePage'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import auth from '../../Requests/auth'
import TopBar from '../TopBar'
import ActivityList from '../../SubComponents/GitHubActivityList/ActivityList'

class Main extends React.Component{

    render() {
        return (
            <AppWrapper>
                <TopBar />
                <ProfilePage object={this.props.object} />
                <ActivityList me={this.props.object}/>
            </AppWrapper>
        );
    }
}

auth.checkLogin();
const url = window.location;
const cb =
    (res) => {
        const myURL = new URL(res.url);
        // if url is '/profile/'
        if (url.pathname === "/profile/"){
            ReactDom.render(<Main object={res}/>,
            document.getElementById('container'));

        // if url is this user's url
        } else if (url.pathname === myURL.pathname){
            window.location.assign('/profile/')

        // if it is other's uuid
        } else{
            const array = url.pathname.split('/');
            const uuid = array[array.length-1];
            GetAuthorRequest.getHim(uuid,
                (object)=> {
                    ReactDom.render(<Main object={object}/>,
                        document.getElementById('container'));
                });
        }

    };

GetAuthorRequest.getMe(cb) ;

