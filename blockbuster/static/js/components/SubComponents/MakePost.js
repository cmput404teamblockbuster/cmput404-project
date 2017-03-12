import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import MakePostContent from './MakePostContent'
import TextField from 'material-ui/TextField'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import Checkbox from 'material-ui/Checkbox'
import FlatButton from 'material-ui/FlatButton'
import PostVisibility from './PostVisibility'
import CreatePostRequest from './CreatePostRequest'

export default class MakePost extends React.Component {
    constructor(props) {
        super(props);

        this.data = {content:"", visibility:"privacy_public"};

        this.changeContent = this.changeContent.bind(this);
        this.changeVisibility = this.changeVisibility.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


    changeContent(data){
        this.data.content = data;
    }

    changeVisibility(data){
        this.data.visibility = data;
        console.log(data)
    }

    handleSubmit(){
        if (this.data.content !== ""){
            CreatePostRequest.send(this.data.content,this.data.visibility)
        }
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title="Make a new post"/>

                <CardMedia>
                    <MakePostContent change={this.changeContent}/>

                    <Toolbar style={{backgroundColor: '#424242'}}>
                        <ToolbarGroup/>
                        <ToolbarGroup >
                            <PostVisibility change={this.changeVisibility}/>
                            {/*<FlatButton style={{margin: '0'}} label="Cancel"  />*/}
                            <FlatButton style={{margin: '0'}} label="Submit" onTouchTap={this.handleSubmit}/>
                        </ToolbarGroup>
                    </Toolbar>

                </CardMedia>
            </Card>
        );
    }
}