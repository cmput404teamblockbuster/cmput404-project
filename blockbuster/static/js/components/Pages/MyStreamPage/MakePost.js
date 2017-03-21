import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import MakePostContent from './MakePostContent'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import FlatButton from 'material-ui/FlatButton'
import PostVisibility from '../../SubComponents/PostList/PostVisibility'
import CreatePostRequest from '../../Requests/CreatePostRequest'
import SelectAuthorButton from './SelectAuthorButton'

export default class MakePost extends React.Component {
    constructor(refresh) {
        // props: refresh: callback function to re-render MyStream
        super(refresh);

        this.state = {content:"", visibility:"privacy_public", button: false};
        this.author = undefined;

        this.changeContent = this.changeContent.bind(this);
        this.changeAuthor = this.changeAuthor.bind(this);
        this.changeVisibility = this.changeVisibility.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.afterSubmit = this.afterSubmit.bind(this);
    }


    changeContent(data){
        this.setState({content:data, button:false});
        this.author = undefined;
    }

    changeAuthor(data){
        this.author = data;
        console.log("makePost: ", data)
    }
    changeVisibility(data){
        if (data === "private_to_one_friend"){
            // TODO: add props to the button
            this.setState({button: <SelectAuthorButton changeAuthor={this.changeAuthor}/>})
        } else {
            this.setState({visibility:data, button:false});
        }


    }

    afterSubmit(){
        if (this.state.visibility === "URL_post"){
            //TODO: Return user a url here
        }
        this.setState({content:"", visibility:"privacy_public", button: false});
        this.author = undefined;
        this.child.changeTab();
        this.props.refresh();
    }

    handleSubmit(){
        if (this.state.content !== ""){
            if (this.state.visibility === "URL_post"){
                //TODO: post an unlisted post
            } else if (this.state.visibility === "private_to_one_friend" && this.author){
                // TODO: post to one single user
            } else {
                CreatePostRequest.send(this.state.content,this.state.visibility, this.afterSubmit)
            }

        }
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title="Make a new post"/>

                <CardMedia>
                    <MakePostContent ref={(input)=>{this.child=input}} change={this.changeContent}/>
                    <Toolbar style={{backgroundColor: '#424242'}}>
                        <ToolbarGroup>
                            {this.state.button}
                        </ToolbarGroup>
                        <ToolbarGroup >
                            <PostVisibility change={this.changeVisibility}/>
                            <FlatButton style={{margin: '0'}} label="Submit" onTouchTap={this.handleSubmit}/>
                        </ToolbarGroup>
                    </Toolbar>
                </CardMedia>
                <CardActions/> /* Just for some margin */
            </Card>
        );
    }
}
