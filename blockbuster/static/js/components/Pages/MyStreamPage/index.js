import React from 'react'
import ReactDom from 'react-dom'
import AppWrapper from '../AppWrapper'
import MyStream from './MyStream'
import TopBar from '../TopBar'

class Main extends React.Component{
    
    render() {
        return (
            <AppWrapper>
                <TopBar />
                <MyStream />
            </AppWrapper>
        );
    }
}

ReactDom.render(<Main />,
document.getElementById('container'));