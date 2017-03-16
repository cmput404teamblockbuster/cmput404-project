import React from 'react'
import {CardText} from 'material-ui/Card'
import Divider from 'material-ui/Divider'
import NameLink from '../PostList/NameLink'

export default class Comment extends React.Component{
    // props: object: {author,body,created,uuid}, changePage
    render(){
        return(
          <CardText className="comment">
            {this.props.object['body']}
            <p style={{color:'#9E9E9E'}}> - by
              <span > <NameLink changePage={this.props.changePage} object={this.props.object['author']}/></span>
              <span > at {this.props.object['created']}</span>
            </p>
          </CardText>
        );
    }
}