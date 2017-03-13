import React from 'react'
import {CardText} from 'material-ui/Card'
import Divider from 'material-ui/Divider'

export default class Comment extends React.Component{
    // props: object: {author,body,created,uuid}
    render(){
        console.log(this.props.object)
        return(
          <CardText className="comment">
            {this.props.object['body']}
            <p style={{color:'#9E9E9E'}}> - by
              <span style={{color:'#82B1FF'}}> {this.props.object['author']['username']}</span>
              <span > at {this.props.object['created']}</span>
            </p>
          </CardText>
        );
    }
}