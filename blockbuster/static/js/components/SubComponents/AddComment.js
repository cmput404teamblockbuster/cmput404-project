import React from 'react'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import TextField from 'material-ui/TextField'
import FlatButton from 'material-ui/FlatButton'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
export default class AddComment extends React.Component{
    //props: refresh: callback function
    render(){
        return(
            <CardMedia>
                <TextField fullWidth={true} multiLine={true} hintText="Write a comment..."/>

                <FlatButton label='Send'/>

            </CardMedia>

        );
    }
}