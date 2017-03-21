import React from 'react'
import ReactDom from 'react-dom'
import SinglePostPage from './SinglePostPage'
import AppWrapper from '../AppWrapper'
import TopBar from '../TopBar'
import PublicTopBar from './PublicTopBar'
import auth from '../../Requests/auth'

class Main extends React.Component{

    render() {
        this.bar = auth.loggedIn()? <TopBar/> : <PublicTopBar/>;
        return (
            <AppWrapper loginPage={true}>
                {this.bar}
                <SinglePostPage />
            </AppWrapper>
        );
    }
}

ReactDom.render(<Main />,
    document.getElementById('container'));