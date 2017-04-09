import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import PostVisibility from './PostVisibility'
import SelectAuthorButton from '../../Pages/MyStreamPage/SelectAuthorButton'
import GetSinglePostRequest from '../../Requests/GetSinglePostRequest'
export default class EditPostDialog extends React.Component{
    constructor(props){
        super(props);

        this.handleClose = this.handleClose.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.changeVisibility = this.changeVisibility.bind(this);
        this.changeAuthor = this.changeAuthor.bind(this);

        this.state = {visibility:"", button:undefined};
        this.actions = [
            <FlatButton label="Cancel" onTouchTap={this.handleClose}/>,
            <FlatButton label="Submit" onTouchTap={this.handleSubmit}/>
        ];
        this.author = undefined;
    }

    handleClose(){
        this.props.refresh();
        this.props.closeAction();
    }

    handleSubmit(){
        GetSinglePostRequest.edit(this.props.postId, this.state.visibility,
            (response)=>{
                this.handleClose();
            }, this.author)
    }

    changeAuthor(data){
        this.author = data;
    }

    changeVisibility(data){
        if (data === "PRIVATE"){
            this.setState({visibility:data, button: <SelectAuthorButton changeAuthor={this.changeAuthor}/>})
        } else {
            this.setState({visibility:data, button:false});
        }
    }

    render(){
        return(
            <Dialog open={true} actions={this.actions} title="Change Privacy" autoScrollBodyContent={true} onRequestClose={this.handleClose}>
                <Toolbar style={{backgroundColor: '#424242'}}>
                    <ToolbarGroup>
                        {this.state.button}
                    </ToolbarGroup>
                    <ToolbarGroup >
                        <PostVisibility change={this.changeVisibility}/>
                    </ToolbarGroup>
                    <ToolbarGroup/>
                </Toolbar>
            </Dialog>
        )}

}

EditPostDialog.propTypes = {
    refresh: React.PropTypes.func.isRequired,
    closeAction: React.PropTypes.func.isRequired,
    postId: React.PropTypes.string.isRequired,
};