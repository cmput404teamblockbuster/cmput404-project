import React from 'react'
import {CardText} from 'material-ui/Card'
import Divider from 'material-ui/Divider'
import NameLink from '../PostList/NameLink'
import moment from 'moment';

export default class Comment extends React.Component{
    // props: object: {author,body,created,uuid}
    render(){
        var time = moment(this.props.object['published']).format("h:mm a dddd, MMMM Do YYYY");
        return(
          <CardText className="comment">
            {this.props.object['comment']}
            <p style={{color:'#9E9E9E'}}> - by
              <span > <NameLink object={this.props.object['author']}/></span>
              <span > at {time}</span>
            </p>
          </CardText>
        );
    }
}