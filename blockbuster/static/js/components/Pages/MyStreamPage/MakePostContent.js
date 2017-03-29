import React from 'react'
import {Tabs, Tab} from 'material-ui/Tabs';
import TextField from 'material-ui/TextField'
import Upload from 'material-ui/svg-icons/file/file-upload'
import FlatButton from 'material-ui/FlatButton'

export default class MakePostContent extends React.Component{
    constructor(props){
        // props: { change: (function) }
        super(props);

        this.state = {uploadText:"Upload Image",contentText:"",markdownText:"" };
        this.changeTab = this.changeTab.bind(this);
        this.handleTitleChange = this.handleTitleChange.bind(this);
        this.handleDescription = this.handleDescription.bind(this);
        this.handleTextChange=this.handleTextChange.bind(this);
        this.handleMarkdownChange = this.handleMarkdownChange.bind(this);
        this.handleImageChange=this.handleImageChange.bind(this);
    }

    changeTab(){
        this.setState({uploadText:"Upload Image",contentText:"", markdownText:"",title:"", description:""});
        this.title = "";
        this.description = "";
    }

    handleTitleChange(event){
        this.title = event.target.value;
        this.props.title(event.target.value);
    }

    handleDescription(event){
        this.description = event.target.value;
        this.props.description(event.target.value)
    }

    handleTextChange(event){
        this.setState({contentText: event.target.value});
        this.props.change(event.target.value, "text/plain");

    }

    handleMarkdownChange(event){
        this.setState({markdownText: event.target.value});
        this.props.change(event.target.value, "text/markdown");
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
                   <TextField id="title" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleTitleChange} hintText="Title" value={this.title}/>
                   <TextField id="description" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleDescription} hintText="Description" value={this.description}/>

                    <TextField id="post-content" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleTextChange} hintText="Content" value={this.state.contentText}/>
                </Tab>
                <Tab label="Markdown Post" value="text">
                   <TextField id="title" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleTitleChange} hintText="Title" value={this.title}/>
                   <TextField id="description" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleDescription} hintText="Description" value={this.description}/>

                    <TextField id="markdown-content" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleMarkdownChange} hintText="Content" value={this.state.markdownText}/>
                </Tab>
                <Tab label="Image Post">
                   <TextField id="title" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleTitleChange} hintText="Title" value={this.title}/>
                   <TextField id="description" hintStyle={{paddingLeft:'20px'}} textareaStyle={{padding:'0px 20px 0px 20px'}}
                               fullWidth={true} multiLine={true} onChange={this.handleDescription} hintText="Description" value={this.description}/>

                    <FlatButton icon={<Upload/>} labelPosition='after' label={this.state.uploadText} containerElement="label" className="fullWidth">
                        <input type="file" accept="image/jpeg, image/png" className="uploadInput" onChange={this.handleImageChange}/>
                    </FlatButton>
                </Tab>
            </Tabs>
        );
    }
}

MakePostContent.propTypes = {
    // change the content of the post in parent
    change: React.PropTypes.func.isRequired,

    // change title
    title: React.PropTypes.func.isRequired,

    // change description
    description: React.PropTypes.func.isRequired,
};