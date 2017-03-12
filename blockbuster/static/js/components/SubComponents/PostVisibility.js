import React from 'react'
import DropDownMenu from 'material-ui/DropDownMenu'
import MenuItem from 'material-ui/MenuItem'

export default class PostVisibility extends React.Component{
    constructor(props){
        // props: {change: function to change the selected value}
        super(props);
        this.state = {visibility:"privacy_public"};

        this.handleChange = this.handleChange.bind(this);

    }

    handleChange(event,key,value){
        this.setState({visibility:value});
        this.props.change(value);
    }

    render(){
        return(
            <DropDownMenu value={this.state.visibility} onChange={this.handleChange} >
                <MenuItem value="private_to_one_friend" primaryText="One Friend"/>
                <MenuItem value="private_to_me" primaryText="Me"/>
                <MenuItem value="private_to_fof" primaryText="Friends-of-Friends"/>
                <MenuItem value="privacy_public" primaryText="Public"/>
                <MenuItem value="private_to_all_friends" primaryText="Friends"/>
            </DropDownMenu>
        );
    }
}