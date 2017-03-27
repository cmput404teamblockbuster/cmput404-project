import React from 'react';

export default class NameLink extends React.Component{
    // changePage, name
    constructor(object){
        super(object);

        this.handleClick = this.handleClick.bind(this);

    }

    handleClick(){
        //
        const array = this.props.object.url.split('/');
        const index = array[array.length-1] === ""? array.length-2:array.length-1
        const uuid = array[index];
        const path = '/profile/' + uuid;
        window.location.assign(path)
    }

    render(){
        return(
            <span onClick={this.handleClick} className="nameLink"> {this.props.object['displayName']}</span>
        );
    }
}