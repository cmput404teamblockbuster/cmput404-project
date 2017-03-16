import React from 'react';

export default class NameLink extends React.Component{
    // changePage, name
    constructor(changePage, object){
        super(changePage,object);

        this.handleClick = this.handleClick.bind(this);

    }

    handleClick(){
        this.props.changePage(3,this.props.object)
    }

    render(){
        return(
            <span onClick={this.handleClick} className="nameLink"> {this.props.object['username']}</span>
        );
    }
}