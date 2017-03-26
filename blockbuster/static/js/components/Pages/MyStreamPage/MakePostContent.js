import React from 'react'
import {Tabs, Tab} from 'material-ui/Tabs';
import TextField from 'material-ui/TextField'
import Upload from 'material-ui/svg-icons/file/file-upload'
import FlatButton from 'material-ui/FlatButton'

export default class MakePostContent extends React.Component{
    constructor(props){
        // props: { change: (function),message}
        super(props);

        this.state = {uploadText:"Upload Image",contentText:this.props.message};

        this.changeTab = this.changeTab.bind(this);
        this.handleTextChange=this.handleTextChange.bind(this);
        this.handleImageChange=this.handleImageChange.bind(this);
    }

    changeTab(){
        this.setState({uploadText:"Upload Image",contentText:""});
    };

    handleTextChange(event){
        this.setState({contentText: event.target.value});
        this.props.change(event.target.value, "text/plain");

    }

    handleImageChange(event){
        console.log("make post content",event.target.files[0]);
        this.reader = new FileReader();
        this.setState({uploadText:event.target.value});
        this.type = event.target.files[0].type + ";base64";
        this.reader.onloadend = ()=>{
            this.props.change(this.reader.result, this.type);

        };
        this.reader.readAsDataURL(event.target.files[0])

    }

    render(){
        return(
            <Tabs ref="hello" onChange={this.changeTab}>
                <Tab label="Text Post" value="text">
                    <TextField id="post-content" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleTextChange} hintText="Content" value={this.state.contentText}/>
                </Tab>
                <Tab label="Image Post">
                    <FlatButton icon={<Upload/>} labelPosition='after' label={this.state.uploadText} containerElement="label" className="fullWidth">
                        <input type="file" accept="image/jpeg, image/png" className="uploadInput" onChange={this.handleImageChange}/>
                    </FlatButton>
                </Tab>
            </Tabs>
        );
    }
}