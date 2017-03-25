import React from 'react'
import { ListItem} from 'material-ui/List';

export default class SearchListItem extends React.Component{
    constructor(object, changePage){
        super(object, changePage);
        this.changePage = this.changePage.bind(this);
    }

    changePage(){
        console.log("search list item");
        console.log(this.props.object);
        this.props.changePage(this.props.object);
    }

    render(){
        return(
            <ListItem primaryText={this.props.object['displayName']} onTouchTap={this.changePage}/>
        );
    }
}