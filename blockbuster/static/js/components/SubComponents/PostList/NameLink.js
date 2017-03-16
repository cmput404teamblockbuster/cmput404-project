import React from 'react';

export default class NameLink extends React.Component{
    // changePage, name
    constructor(object){
        super(object);

        this.handleClick = this.handleClick.bind(this);

    }

    handleClick(){
        const path = '/profile?' + this.props.object['uuid'];
        window.location.assign(path)
    }

    render(){
        return(
            <span onClick={this.handleClick} className="nameLink"> {this.props.object['username']}</span>
        );
    }
}