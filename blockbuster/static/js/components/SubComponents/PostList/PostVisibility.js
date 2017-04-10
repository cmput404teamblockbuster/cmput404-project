import React from 'react'
import DropDownMenu from 'material-ui/DropDownMenu'
import MenuItem from 'material-ui/MenuItem'

export default class PostVisibility extends React.Component{
    constructor(props){
        // props: {change: function to change the selected value}
        super(props);
        this.state = {visibility:"PUBLIC"};

        this.handleChange = this.handleChange.bind(this);

        if (this.props.edit===true){
            this.privateTo = false
        } else {
            this.privateTo = <MenuItem value="PRIVATE" primaryText="Private To"/>
        }

    }

    handleChange(event,key,value){
        console.log("post visibility", value)
        this.setState({visibility:value});
        this.props.change(value);
    }

    render(){
        /* TODO change something here */
        return(
            <DropDownMenu value={this.state.visibility} onChange={this.handleChange} >
                <MenuItem value="PUBLIC" primaryText="Share With Public"/>
                {this.privateTo}
                <MenuItem value="FRIENDS" primaryText="Share With Friends"/>
                <MenuItem value="SERVERONLY" primaryText="Share With Local Friends"/>
                <MenuItem value="FOAF" primaryText="Share With FOAF"/>

                {/* I mean here */}
                <MenuItem value="privacy_unlisted" primaryText="Link Access Only"/>
            </DropDownMenu>
        );
    }
}