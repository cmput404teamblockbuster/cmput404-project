import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import CommentSection from './CommentSection'
import AddComment from './AddComment'

export default class PostContainer extends React.Component{
    constructor(object,refresh){
        super(object,refresh);

        // this.state = {refresh:true};
        //
        // this.componentWillMount = this.componentWillMount.bind(this);
    }

    // componentWillMount(){
    //     this.setState({refresh:!this.state.refresh});
    // }

    render(){
        return(
            <li>
                <Card className="textField">
                    <CardHeader title={this.props.object['author']['username']} titleColor={'#82B1FF'} /><Divider/>
                    <CardText >
                        <p className="postBody">{this.props.object['content']}</p>
                    </CardText>
                    <Divider/>
                    <CardMedia>
                        <CommentSection postid={this.props.object['uuid']} object={this.props.object['comments']} refresh={this.props.refresh}/>
                    </CardMedia>
                </Card>
            </li>
        );
    }
}