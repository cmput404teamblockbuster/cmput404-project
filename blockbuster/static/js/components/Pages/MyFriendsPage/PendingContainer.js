import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import NameLink from '../../SubComponents/PostList/NameLink'
import RespondToPending from './RespondToPending'
import FlatButton from 'material-ui/FlatButton'

export default class PendingContainer extends React.Component{
    constructor(object,refresh){
        super(object,refresh);
    }

    render(){
        return(
            <li>
                <Card className="textField" style={{paddingBottom:'5px'}}>
                    <CardHeader title={<NameLink object={this.props.object['initiator']}/>}/>
                    <RespondToPending relation={this.props.object} refresh={this.props.refresh}/>
                </Card>
            </li>
        );
    }
}