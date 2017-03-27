import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import SearchUserDialog from '../../SubComponents/Search/SearchUserDialog';

export default class SelectAuthorButton extends React.Component{
    //props: changeAuthor:func,
    constructor(props){
        super(props);

        this.state = {labelText: "Select An Author", dialog:false};
        this.closeDialog = this.closeDialog.bind(this);
        this.getAuthor = this.getAuthor.bind(this);
        this.openDialog = this.openDialog.bind(this);
    }

    closeDialog(){
        this.setState({dialog:false});
    }

    openDialog(){
        this.setState(
            {dialog: <SearchUserDialog open={true} closeAction={this.closeDialog}
                                       changePage={this.getAuthor} />}
        )
    }

    getAuthor(object){
        this.setState({labelText:object.displayName, dialog:false});
        this.props.changeAuthor(object)
    }


    render(){
        return(
            <RaisedButton primary={true} style={{margin: '0'}} label={this.state.labelText} onTouchTap={this.openDialog}>
                {this.state.dialog}
            </RaisedButton>
        );
    }
}

SelectAuthorButton.propTypes = {
    /** a callback function that will be called with a user object **/
    changeAuthor: React.PropTypes.func.isRequired,
};