import React from 'react'
import DropDownMenu from 'material-ui/DropDownMenu'
import MenuItem from 'material-ui/MenuItem'

export default class PostVisibility extends React.Component{
    constructor(props){
        // props: {change: function to change the selected value}
        super(props);
        this.state = {visibility:"PUBLIC"};

        this.handleChange = this.handleChange.bind(this);

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
                <MenuItem value="PUBLIC" primaryText="Share To Public"/>
                <MenuItem value="PRIVATE" primaryText="Private to"/>
                <MenuItem value="FRIENDS" primaryText="Share To Friends"/>
                <MenuItem value="SERVERONLY" primaryText="Share To local Friends"/>
                <MenuItem value="FOAF" primaryText="Share To FoF"/>

                {/* I mean here */}
                <MenuItem value="privacy_unlisted" primaryText="Sharable Post"/>
            </DropDownMenu>
        );
    }
}