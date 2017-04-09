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

        this.state = {content:"", contentType:"text/plain", visibility:"PUBLIC", button: false, title:"", description:""};
        this.author = undefined;

        this.changeTitle = this.changeTitle.bind(this);
        this.changeDescription = this.changeDescription.bind(this);
        this.changeContent = this.changeContent.bind(this);
        this.changeAuthor = this.changeAuthor.bind(this);
        this.changeVisibility = this.changeVisibility.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.afterSubmit = this.afterSubmit.bind(this);
    }

    changeTitle(data){
        this.setState({title:data})
    }

    changeDescription(data){
        this.setState({description:data})
    }

    changeContent(data, type){
        this.setState({content:data, contentType: type});
    }

    changeAuthor(data){
        this.author = data;
    }

    changeVisibility(data){
        if (data === "PRIVATE"){
            this.setState({visibility:data, button: <SelectAuthorButton changeAuthor={this.changeAuthor}/>})
        } else {
            this.author = undefined;
            this.setState({visibility:data, button:false});
        }


    }

    afterSubmit(res){
        if (this.state.visibility === "privacy_unlisted"){
            //TODO: Return user a url here
            const host = window.location.host;
            const url = host+'/post/'+res['id'] ;
            alert("your url is: " + url)
        }
        this.setState({content:"", title:"", description:""});
        this.child.changeTab();
        this.props.refresh();
    }

    handleSubmit(){
        if (this.state.content !== ""){
            if (this.state.visibility === "PRIVATE" && this.author){
                // post to one single user TODO: make sure users on other server as well
                CreatePostRequest.send(this.state.content, this.state.title, this.state.description,
                    this.state.contentType, this.state.visibility, this.afterSubmit, this.author)
            } else {
                CreatePostRequest.send(this.state.content, this.state.title, this.state.description,
                    this.state.contentType, this.state.visibility, this.afterSubmit)
            }

        }
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title="Make a new post"/>

                <CardMedia>
                    <MakePostContent ref={(input)=>{this.child=input}} change={this.changeContent}
                                     title={this.changeTitle} description={this.changeDescription}/>
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
