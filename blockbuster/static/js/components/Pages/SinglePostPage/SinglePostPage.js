import React from 'react'
import Paper from 'material-ui/Paper'
import AppBar from 'material-ui/AppBar'


export default class SinglePostPage extends React.Component{
    constructor(object){
        // props: object
        super(object);

    }

    componentWillMount(callback){

    }


    render(){
        return(
            <Paper className="streamContainer">
                <AppBar className="title" title="A Post" iconElementLeft={<div/>}/>
                <ul className="mainList">

                </ul>
            </Paper>
        );
    }
}