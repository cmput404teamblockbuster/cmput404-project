import React from 'react'
import WithdrawPendingToolbar from '../../SubComponents/RelationshipToolbars/WithdrawPendingToolbar'
import AcceptRejectToolbar from '../../SubComponents/RelationshipToolbars/AcceptRejectToolbar'
import UnFriendToolbar from '../../SubComponents/RelationshipToolbars/UnFriendToolbar'
import BefriendToolbar from '../../SubComponents/RelationshipToolbars/BefriendToolbar'
import UnfollowToolbar from '../../SubComponents/RelationshipToolbars/UnfollowToolbar'
import NameLink from '../../SubComponents/PostList/NameLink'
import {Toolbar, ToolbarGroup, ToolbarTitle} from 'material-ui/Toolbar';

export default class ListItemContainer extends React.Component{
    constructor(props){
        super(props);

        // if (this.props.status === "friends"){
        //     this.state = {toolbar:<UnFriendToolbar object={this.props.object} refresh={this.props.refresh}/>}
        // } else if (this.props.status === "requested"){
        //     this.state = {toolbar:<AcceptRejectToolbar object={this.props.object} refresh={this.props.refresh}/>}
        // } else {
        //     this.state = {toolbar:false}
        // }
    }
    render(){
        return(
            <li style={{backgroundColor:'#424242', textAlign:'center', border:'solid #4FC3F7'}}>
                {/*<Toolbar style={{backgroundColor:'#424242', textAlign:'center', border:'solid #4FC3F7'}}>*/}
                    {/*<ToolbarGroup>*/}
                        <NameLink object={this.props.object}/>
                    {/*</ToolbarGroup>*/}
                    {/*/!*<ToolbarGroup>*!/*/}
                    {/*/!*</ToolbarGroup>*!/*/}
                {/*</Toolbar>*/}
            </li>
        );
    }
}

ListItemContainer.propTypes = {
    status: React.PropTypes.string.isRequired,
    refresh: React.PropTypes.func.isRequired,
    object: React.PropTypes.object.isRequired,
};