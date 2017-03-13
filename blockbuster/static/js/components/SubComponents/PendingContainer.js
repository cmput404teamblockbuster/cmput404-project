import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import NameLink from './NameLink'
import RespondToPending from './RespondToPending'
import FlatButton from 'material-ui/FlatButton'

export default class PendingContainer extends React.Component{
    constructor(object,refresh, changePage){
        super(object,refresh, changePage);
    }

    render(){
        return(
            <li>
                <Card className="textField">
                    <CardHeader title={<NameLink changePage={this.props.changePage} object={this.props.object['initiator']}/>}/>
                    <Divider/>
                    <RespondToPending relation={this.props.object} refresh={this.props.refresh}/>
                </Card>
            </li>
        );
    }
}