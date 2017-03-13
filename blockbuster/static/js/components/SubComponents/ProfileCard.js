import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
// import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import Divider from 'material-ui/Divider'

export default class ProfileCard extends React.Component {
    constructor(object) {
        // props: refresh: callback function to re-render MyStream
        super(object);

        this.state = {username:this.props.object['username'],
            github:this.props.object['github'] ? this.props.object['github'] : "Don't have one yet" };
    }


    render() {
        return (
            <Card className="textField">
                <CardHeader title={"Username: "+this.state.username}/>
                <Divider/>
                <CardHeader title={"Github  : "+this.state.github}/>
            </Card>
        );
    }
}