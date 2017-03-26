import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import PublicPosts from './PublicPosts'
import TopBar from '../TopBar'

class Main extends React.Component{

    render() {
        return (
            <AppWrapper>
                <TopBar />
                <PublicPosts />
            </AppWrapper>
        );
    }
}

ReactDom.render(<Main />,
document.getElementById('container'));