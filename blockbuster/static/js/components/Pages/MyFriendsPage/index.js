import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import MyFriends from './MyFriends'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'
import TopBar from '../TopBar'

class Main extends React.Component{
    render() {
        return (
            <AppWrapper>
                <TopBar />
                <MyFriends object={this.props.object} />
            </AppWrapper>
        );
    }
}


GetAuthorRequest.getMe(
    (author)=> {
        ReactDom.render(<Main object={author}/>,
            document.getElementById('container'));
    }
);
