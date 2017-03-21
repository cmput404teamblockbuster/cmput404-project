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
        /* TODO change something here */
        return(
            <DropDownMenu value={this.state.visibility} onChange={this.handleChange} >
                <MenuItem value="privacy_public" primaryText="Share To Public"/>
                <MenuItem value="private_to_me" primaryText="Share To Me Only"/>
                <MenuItem value="private_to_all_friends" primaryText="Share To Friends"/>
                <MenuItem value="private_to_fof" primaryText="Share To FoF"/>

                {/* I mean here */}
                <MenuItem value="private_to_one_friend" primaryText="Share To An Author"/>
                <MenuItem value="privacy_unlisted" primaryText="Sharable Post"/>
            </DropDownMenu>
        );
    }
}