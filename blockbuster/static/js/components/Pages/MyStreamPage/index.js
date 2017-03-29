import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import MyStream from './MyStream'
import TopBar from '../TopBar'
import ActivityList from '../../SubComponents/GitHubActivityList/ActivityList'
import GetAuthorRequest from '../../Requests/GetAuthorRequest'

class Main extends React.Component{
    
    render() {
        return (
            <AppWrapper>
                <TopBar />
                <MyStream me={this.props.me}/>
                <ActivityList me={this.props.me}/>
            </AppWrapper>
        );
    }
}

GetAuthorRequest.getMe((Me)=>{
    ReactDom.render(<Main me={Me}/>,
        document.getElementById('container'));
});
