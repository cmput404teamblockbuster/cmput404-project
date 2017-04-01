import React from 'react';
import {CardActions, CardMedia, CardHeader} from 'material-ui/Card'
import ReactMarkdown from 'react-markdown'
import FlatButton from 'material-ui/FlatButton'
import Last from 'material-ui/svg-icons/navigation/chevron-left'
import Next from 'material-ui/svg-icons/navigation/chevron-right'

export default class ListBody extends React.Component{
    constructor(props){
        super(props);

        this.previousPage = this.previousPage.bind(this);
        this.nextPage = this.nextPage.bind(this);
    }

    previousPage(){
        this.props.changePage(false);
    }

    nextPage(){
        this.props.changePage(true);
    }

    render(){
        const body = this.props.listOfObjects.map((activity,index)=><li key={index}><ReactMarkdown source={activity}/></li>);
        return(
            <div>
                <CardHeader avatar={this.props.actor.avatar_url} title={this.props.actor.login}/>
                <ul className="mainList" id="scrollable">
                {body}
                </ul>
                <FlatButton icon={<Last/>} label="Previous" className="previousButton" onTouchTap={this.previousPage}/>
                {/*<span style={{padding:'0 11px 0 11px'}} >{this.props.page}</span>*/}
                <FlatButton icon={<Next/>} label="Next" labelPosition='before' className="nextButton" onTouchTap={this.nextPage}/>
            </div>

        )
    }
}

ListBody.propTypes = {
    // the author
    actor: React.PropTypes.object.isRequired,

    changePage: React.PropTypes.func.isRequired,

    listOfObjects: React.PropTypes.array.isRequired,

    page: React.PropTypes.number.isRequired,
};