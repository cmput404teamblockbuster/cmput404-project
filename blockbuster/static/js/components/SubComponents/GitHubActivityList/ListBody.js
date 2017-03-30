import React from 'react';
import {CardActions, CardMedia, CardHeader} from 'material-ui/Card'
import ReactMarkdown from 'react-markdown'
import FlatButton from 'material-ui/FlatButton'
import Last from 'material-ui/svg-icons/navigation/chevron-left'
import Next from 'material-ui/svg-icons/navigation/chevron-right'

export default class ListBody extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const body = this.props.listOfObjects.map((activity,index)=><li key={index}><ReactMarkdown source={activity}/></li>);
        return(
            <ul className="mainList" id="scrollable">
                <CardHeader avatar={this.props.actor.avatar_url} title={this.props.actor.login}/>
                {body}
            </ul>
        )
    }
}

ListBody.propTypes = {
    // the author
    actor: React.PropTypes.object.isRequired,

    changePage: React.PropTypes.func.isRequired,

    listOfObjects: React.PropTypes.array.isRequired,

    page: React.PropTypes.number.isRequired,
};