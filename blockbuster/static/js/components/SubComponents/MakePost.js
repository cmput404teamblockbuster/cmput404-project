import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import MakePostContent from './MakePostContent'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import FlatButton from 'material-ui/FlatButton'
import PostVisibility from './PostVisibility'
import CreatePostRequest from './CreatePostRequest'

export default class MakePost extends React.Component {
    constructor(refresh) {
        // props: refresh: callback function to re-render MyStream
        super(refresh);

        this.state = {content:"", visibility:"privacy_public"};
        this.changeContent = this.changeContent.bind(this);
        this.changeVisibility = this.changeVisibility.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.afterSubmit = this.afterSubmit.bind(this);
    }


    changeContent(data){
        this.setState({content:data});
    }

    changeVisibility(data){
        this.setState({visibility:data});
        console.log(data)
    }

    afterSubmit(){
        this.setState({content:""});
        this.child.changeTab();
        this.props.refresh();
    }

    handleSubmit(){
        if (this.state.content !== ""){
            CreatePostRequest.send(this.state.content,this.state.visibility, this.afterSubmit)
        }
    }

    render() {
        return (
            <Card className="textField" style={{backgroundColor:'#424242'}}>
                <CardHeader title="Make a new post"/>

                <CardMedia>
                    <MakePostContent ref={(input)=>{this.child=input}} change={this.changeContent}/>
                    <Toolbar style={{backgroundColor: '#424242'}}>
                        <ToolbarGroup/>
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