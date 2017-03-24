import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import ProfilePage from './ProfilePage'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import TopBar from '../TopBar'

class Main extends React.Component{

    render() {
        return (
            <AppWrapper>
                <TopBar />
                <ProfilePage object={this.props.object} />
            </AppWrapper>
        );
    }
}

const url = window.location;
const cb =
    (res) => {
        // if url is '/profile/'
        if (url.pathname === "/profile/"){
            ReactDom.render(<Main object={res}/>,
            document.getElementById('container'));

        // if url is this user's url
        } else if (res['url'] === url){
            window.location.assign('/profile/')

        // if it is other's uuid
        } else{
            const array = url.pathname.split('/');
            const uuid = array[array.length-1];
            GetAuthorRequest.getHim(url.pathname,
                (object)=> {
                    ReactDom.render(<Main object={object}/>,
                        document.getElementById('container'));
                });
        }

    };

GetAuthorRequest.getMe(cb) ;

