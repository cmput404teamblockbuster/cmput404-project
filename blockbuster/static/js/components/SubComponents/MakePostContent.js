import React from 'react'
import {Tabs, Tab} from 'material-ui/Tabs';
import TextField from 'material-ui/TextField'
import Upload from 'material-ui/svg-icons/file/file-upload'
import FlatButton from 'material-ui/FlatButton'

export default class MakePostContent extends React.Component{
    constructor(props){
        // props: { change: (function)}
        super(props);

        this.state = {uploadText:"Upload Image"};
        this.contentText = "";

        this.changeTab = this.changeTab.bind(this);
        this.handleTextChange=this.handleTextChange.bind(this);
        this.handleImageChange=this.handleImageChange.bind(this);
    }

    changeTab(){
        this.contentText = "";
        this.setState({uploadText:"Upload Image"});
    };

    handleTextChange(event){
        this.contentText = event.target.value;
        this.props.change(event.target.value);

    }

    handleImageChange(event){
        this.props.change(event.target.value);
        this.setState({uploadText:event.target.value})
    }

    render(){
        return(
            <Tabs onChange={this.changeTab}>
                <Tab label="Text Post" value="text">
                    <TextField hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleTextChange} hintText="Content"/>
                </Tab>
                <Tab label="Image Post">
                    <FlatButton icon={<Upload/>} labelPosition='after' label={this.state.uploadText} containerElement="label" className="fullWidth">
                        <input type="file" accept="image/*" className="uploadInput" onChange={this.handleImageChange}/>
                    </FlatButton>
                </Tab>
            </Tabs>
        );
    }
}