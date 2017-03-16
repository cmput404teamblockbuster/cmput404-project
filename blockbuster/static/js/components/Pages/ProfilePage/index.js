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

const uuid = window.location.search.substring(1);
const cb =
    (res) => {
        // if url is '/profile/'
        if (!uuid){
            ReactDom.render(<Main object={res}/>,
            document.getElementById('container'));

        // if url is '/profile/<my_uuid>/'
        } else if (res['uuid'] === uuid){
            window.location.assign('/profile/')

        // if it is other's uuid
        } else{
            GetAuthorRequest.getHim(uuid,
                (object)=> {
                    ReactDom.render(<Main object={object}/>,
                        document.getElementById('container'));
                });
        }

    };

GetAuthorRequest.getMe(cb) ;

