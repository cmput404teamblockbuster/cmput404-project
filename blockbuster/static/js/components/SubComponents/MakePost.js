import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import MakePostContent from './MakePostContent'
import TextField from 'material-ui/TextField'
import {Toolbar, ToolbarGroup} from 'material-ui/Toolbar'
import Checkbox from 'material-ui/Checkbox'
import FlatButton from 'material-ui/FlatButton'

export default class MakePost extends React.Component {
    constructor(props) {
        super(props);

        this.state = {title: "", public:true}
    }

    render() {
        return (
            <Card className="textField">
                <CardHeader title="Make a new post"/>

                <CardMedia>
                    <TextField hintStyle={{paddingLeft: '20px'}} textareaStyle={{padding: '0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handle} hintText="Title"/>
                    <MakePostContent/>
                    <Toolbar style={{backgroundColor: '#424242'}}>
                        <ToolbarGroup/>
                        <ToolbarGroup >
                            <Checkbox style={{margin: '20px', width: 'auto'}} checked={this.state.public} label="public"
                                      />
                            <FlatButton style={{margin: '0'}} label="Cancel" labelStyle={{color: 'grey'}}
                                        />
                            <FlatButton style={{margin: '0'}} label="Submit" labelStyle={{color: 'grey'}}
                                        />
                        </ToolbarGroup>
                    </Toolbar>
                </CardMedia>
                <CardActions>

                </CardActions>
            </Card>
        );
    }
}