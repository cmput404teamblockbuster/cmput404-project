import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Divider from 'material-ui/Divider';
import CommentSection from './CommentSection'
import NameLink from './NameLink'

export default class PostContainer extends React.Component{
    constructor(object,refresh, changePage){
        super(object,refresh, changePage);

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
                    {/*<CardHeader title={this.props.object['author']['username']} titleColor={'#82B1FF'} /><Divider/>*/}
                    <CardHeader title={<NameLink changePage={this.props.changePage} object={this.props.object['author']}/>}/><Divider/>
                    <CardText >
                        <p className="postBody">{this.props.object['content']}</p>
                    </CardText>
                    <Divider/>
                    <CardMedia>
                        <CommentSection changePage={this.props.changePage} postid={this.props.object['uuid']} object={this.props.object['comments']} refresh={this.props.refresh}/>
                    </CardMedia>
                </Card>
            </li>
        );
    }
}