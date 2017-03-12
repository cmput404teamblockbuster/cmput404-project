import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import MakePostContent from './MakePostContent'
import TextField from 'material-ui/TextField'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import Checkbox from 'material-ui/Checkbox'
import FlatButton from 'material-ui/FlatButton'
import PostVisibility from './PostVisibility'

export default class MakePost extends React.Component {
    constructor(props) {
        super(props);

        this.data = {content:"", visibility:"public"};
        // this.data = {title:"", content:"", visibility:"public"};
        // this.changeTitle = this.changeTitle.bind(this);
        this.changeContent = this.changeContent.bind(this);
        this.changeVisibility = this.changeVisibility.bind(this);
    }

    // changeTitle(event){
    //     this.data.title = event.target.value;
    // }

    changeContent(data){
        this.data.content = data;
    }

    changeVisibility(data){
        this.data.visibility = data;
        console.log(data)
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title="Make a new post"/>

                <CardMedia>
                    {/*<TextField hintStyle={{paddingLeft: '20px'}} textareaStyle={{padding: '0px 20px 0px 20px'}}*/}
                               {/*fullWidth={true} multiLine={true} onChange={this.changeTitle} hintText="Title"/>*/}
                    <MakePostContent change={this.changeContent}/>

                    <Toolbar style={{backgroundColor: '#424242'}}>
                        <ToolbarGroup/>
                        <ToolbarGroup >
                            <PostVisibility change={this.changeVisibility}/>
                            <FlatButton style={{margin: '0'}} label="Cancel"  />
                            <FlatButton style={{margin: '0'}} label="Submit" />
                        </ToolbarGroup>
                    </Toolbar>

                </CardMedia>
            </Card>
        );
    }
}