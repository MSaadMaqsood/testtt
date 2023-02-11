import React, { Component } from "react";
import TopNavbar from "../../global/components/navbar";
import Exe_MiniDrawer from "../../global/components/exe_Sidebar";
import Card from "react-bootstrap/Card";
import "./index.css";
import { useNavigate } from "react-router-dom";
import { Button, Modal, Input } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import Form from "react-bootstrap/Form";
import InputGroup from 'react-bootstrap/InputGroup';
export default class UserManagement extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show_users: [],
      users:[],
      list_of_cities: {},
      add_new_user_model: false,
      edit_user_model: false,

      filter_table: {
        fullname: "",
        position: ""
      },
      add_new_user_form:{
        fullname: "",
        username:"",
        password:"",
        position:"",
        cities:{}
      },
      edit_user_form:{
        user_id:0,
        fullname: "",
        username:"",
        password:"",
        position:"",
        cities:{}
      }
     }
    this.GetData = this.GetData.bind(this);
    this.AddUserData = this.AddUserData.bind(this);
    this.UpdateUserData = this.UpdateUserData.bind(this);
    this.apply_filter = this.apply_filter.bind(this);
    this.reset_filter = this.reset_filter.bind(this);
    this.handleChange_fullname = this.handleChange_fullname.bind(this);
    this.handleChange_pos = this.handleChange_pos.bind(this);
    this.hide_add_new_user_model = this.hide_add_new_user_model.bind(this);
     this.hide_edit_user_model = this.hide_edit_user_model.bind(this);
    this.reset_add_new_user_model = this.reset_add_new_user_model.bind(this);


    this.onChangeCitiesValue = this.onChangeCitiesValue.bind(this);
    this.onChangePositionValue = this.onChangePositionValue.bind(this);
    this.onChangeTextField = this.onChangeTextField.bind(this);

    this.onChangeCitiesValue_edit_user = this.onChangeCitiesValue_edit_user.bind(this);
    this.onChangePositionValue_edit_user = this.onChangePositionValue_edit_user.bind(this);
    this.onChangeTextField_edit_user = this.onChangeTextField_edit_user.bind(this);
    this.GetData();
  }

  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server + "/get_userlog_list_all")
      .then(function (response) {
        com.setState({
          users: response.data.users,
          show_users: response.data.users,
          list_of_cities: response.data.cities
        });
      });
  }

  AddUserData() {
    const com = this;
    const axios = require("axios").default;
    const info = this.state.add_new_user_form;
    
    if(info.fullname == "" || info.username=="" || info.password=="" || info.position==""){
      alert("No Information can be empty!");
    }else{

        const json_info = {
          
          "fullname": info.fullname,
          "username":info.username,
          "password":info.password,
          "position":info.position,
          "cities":info.cities
        }
        axios
          .post(this.props.server + "/add_new_user", json_info)
          .then(function (response) {
            if(response.data.r == 2){
              alert("Username already Exists!");
            }else if(response.data.r == 1){
              alert("User Added!");
              com.reset_add_new_user_model();
              com.GetData();
            }else if(response.data.r == 0){
              alert("Failed while User Adding!");
            }
          });
    }
  }
  UpdateUserData() {
    const com = this;
    const axios = require("axios").default;
    const info = this.state.edit_user_form;
    
    if(info.fullname == "" || info.username=="" || info.password=="" || info.position==""){
      alert("No Information can be empty!");
    }else{

        const json_info = {
          "user_id":info.user_id,
          "fullname": info.fullname,
          "username":info.username,
          "password":info.password,
          "position":info.position,
          "cities":info.cities
        }
        axios
          .post(this.props.server + "/update_user_info", json_info)
          .then(function (response) {
            if(response.data.r == 2){
              alert("Username already Exists!");
            }else if(response.data.r == 1){
              alert("User Updated!");
              com.reset_add_new_user_model();
              com.GetData();
            }else if(response.data.r == 0){
              alert("Failed while User Updating!");
            }
          });
    }
  }

  EditUserData(userid) {
    const com = this;
    const axios = require("axios").default;
    const json_info = {
      "user_id": userid,
      "cities": this.state.list_of_cities 
    }
    axios
      .post(this.props.server + "/get_user_info", json_info)
      .then(function (response) {
        com.setState({
          edit_user_form: response.data.user,
          edit_user_model:true
        })
      });

  }
  apply_filter(){

    let filter_data = [];
    if (this.state.filter_table.fullname == ""){
        filter_data = this.state.users;
    }else{
        this.state.users.forEach(element => {
            if(element.fullname.indexOf(this.state.filter_table.fullname) > -1){
                filter_data.push(element);
            }
        });
    }
    if (this.state.filter_table.position == ""){
    }else{
        let tempx = [];
        
        filter_data.forEach(element => {
          
            if(element.position.indexOf(this.state.filter_table.position) > -1){
                tempx.push(element);
            }
        });
        filter_data = tempx;
    }
    
    this.setState({
        show_users: filter_data
    });
  }
hide_add_new_user_model(){
  this.setState({
    add_new_user_model:false,
    add_new_user_form:{
      fullname: "",
      username:"",
      password:"",
      position:"",
      cities:this.state.list_of_cities
    }
  })
}
hide_edit_user_model(){
  this.setState({
    edit_user_model:false,
    edit_user_form:{
      fullname: "",
      username:"",
      password:"",
      position:"",
      cities:{}
    }
  })
}
  reset_filter(){
    let temp = this.state.users;
    this.setState({
      show_users: temp,
      filter_table: {
        fullname: "",
        position: ""
      }
    })
  }
  handleChange_fullname(e){
    let xx= this.state.filter_table;
    xx.fullname = e.target.value;
    this.setState({
        filter_table:xx
    }); 
  }
  handleChange_pos(e){
    let xx= this.state.filter_table;
    xx.position = e.target.value;
    this.setState({
        filter_table:xx
    }); 
  }
  onChangeTextField(event, textfield){
    let xx = this.state.add_new_user_form;
    if(textfield === "fullname"){
      xx.fullname = event.target.value;
    }else if(textfield === "username"){
      xx.username = event.target.value;
    }else if(textfield === "pwd"){
      xx.password = event.target.value;
    }
    this.setState({add_new_user_form: xx});
  }
  onChangePositionValue(event) {
    
    let xx = this.state.add_new_user_form;
    xx.position = event.target.value;
    this.setState({add_new_user_form: xx});
    console.log(xx);
  }
  onChangeCitiesValue(event) {
    console.log(event.target.value);
    let xx = this.state.add_new_user_form;
    xx.cities[event.target.value] = !(xx.cities[event.target.value]);
    this.setState({add_new_user_form: xx});
    console.log(xx);
  }
  //////////////////////
  onChangeTextField_edit_user(event, textfield){
    let xx = this.state.edit_user_form;
    if(textfield === "fullname"){
      xx.fullname = event.target.value;
    }else if(textfield === "username"){
      xx.username = event.target.value;
    }else if(textfield === "pwd"){
      xx.password = event.target.value;
    }
    this.setState({edit_user_form: xx});
  }
  onChangePositionValue_edit_user(event) {
    
    let xx = this.state.edit_user_form;
    xx.position = event.target.value;
    this.setState({edit_user_form: xx});
    
  }
  onChangeCitiesValue_edit_user(event) {
    
    let xx = this.state.edit_user_form;
    xx.cities[event.target.value] = !(xx.cities[event.target.value]);
    this.setState({edit_user_form: xx});
  }
  reset_add_new_user_model(){
    this.setState({
      add_new_user_form:{
        fullname: "",
        username:"",
        password:"",
        position:"",
        cities:this.state.list_of_cities
      }
    })
  }
  render() {
  return (
    <div>
      <Exe_MiniDrawer />
      <TopNavbar />
      <Card className="card_bg" style={{marginLeft:"7%",marginTop:"-5%",paddingRight:"20px",marginRight:"20px"}}>
      <div className="verifier_cases_details_table">
      <center> <h2>User Information Table</h2></center>
      <div style={{width:"100%",height:"40px"}}>
        <button type="button" class="btn btn-danger mb-3"  onClick={()=>{this.setState({add_new_user_model:true})}}  style={{width:"150px",float:"right"}}>Add User </button>
      </div>
       <hr />
       <div style={{display:"flex",flexDirection:"row", paddingRight:"50px"}}>
            <div class="input-group mb-3"  style={{width:"300px",marginLeft:"10px"}}>
                <span class="input-group-text" id="basic-addon1">Full name </span>
                <input type="text" class="form-control" value={this.state.filter_table.fullname} onChange={this.handleChange_fullname} />
            </div>
            <div class="input-group mb-3"  style={{width:"300px",marginLeft:"10px"}}>
                <span class="input-group-text" id="basic-addon1">Position </span>
                <input type="text" class="form-control" value={this.state.filter_table.position} onChange={this.handleChange_pos} />
            </div>
            <button type="button" class="btn btn-primary mb-3"  onClick={this.apply_filter}  style={{width:"150px"}}>Filter </button>
            <button type="button" class="btn btn-danger mb-3"  onClick={this.reset_filter}  style={{width:"150px"}}>Reset Filter </button>
            
       </div>
       <br />
        <div class="row">
        
          <div class="verifier-table-responsive " style={{ paddingBottom:"15px",paddingRight:"25px" }}>
            
            <table class="table table-striped table-hover table-bordered">
              <thead>
                <tr>
                  <th style={{ fontFamily: "Verdana" }}>User ID</th>
                  <th style={{ fontFamily: "Verdana" }}>
                    Full name{" "}
                  </th>
                  <th>Position</th>
                  <th>Allowed Cities</th>
                  <th style={{ fontFamily: "Verdana" }}></th>
                </tr>
              </thead>
              <tbody>
                {
                  this.state.show_users.map((x)=>(
                    <tr>
                    <td>{x.user_id}</td>
                    <td>{x.fullname}</td>
                    <td>{x.position}</td>
                    <td>{x.city_allow}</td>
                    <td>
                    <Button
                        variant="danger"
                        style={{ height: "60%" }}
                        onClick={() => {this.EditUserData(x.user_id);}}
                      >
                        Edit
                      </Button>
                      {" "}
                      <Button
                        variant="primary"
                        style={{ height: "60%" }}
                        onClick={() =>{  window.location.href ="/usermanagement/userlog/"+x.user_id;  }}
                      >
                        View Log Details
                      </Button>
                    </td>
                  </tr>
                  ))
                }
              </tbody>
            </table>
            
          </div>
        </div>
      </div>
      </Card>
      <div style={{ width: "100%" }} className="model_box">
          <Modal
            dialogClassName="modal_width_styles"
            contentClassName="modal_height_styles"
            isOpen={this.state.add_new_user_model}
            onRequestClose={this.hide_add_new_user_model}
            show={this.state.add_new_user_model}
            onHide={this.hide_add_new_user_model}
            keyboard={false}
            style={{ width: "100%", height: "100%" }}
          >
            <Modal.Header closeButton>
              <Modal.Title>
                Add New User
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Form>
              <Form.Group className="mb-2">
                  <Form.Label>User Fullname</Form.Label>
                  <Form.Control
                    value={this.state.add_new_user_form.fullname}
                    onChange={(e) => this.onChangeTextField(e, "fullname")}

                  />
                </Form.Group>
              <table className="model_table_">
                
              <tr className="model_table_row">
                    <td className="model_table_data">
                <Form.Group className="mb-2">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    value={this.state.add_new_user_form.username}
                    onChange={(e) => this.onChangeTextField(e, "username")}
                  />
                </Form.Group>
                </td>
                <td className="model_table_data">
                <Form.Group className="mb-2">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    value={this.state.add_new_user_form.password}
                    onChange={(e) => this.onChangeTextField(e, "pwd")}
                  />

                </Form.Group>
                </td>
                </tr>
                </table>
                 
                <Form.Group className="mb-6">
                  <Form.Label>Position</Form.Label>
                  <center>
                    <tr>
                        <td>
                          <InputGroup  style={{width:"150px",padding:"5px"}}>
                            <InputGroup.Radio aria-label="Checkbox for following text input" value="Executive" name="group1" checked = {this.state.add_new_user_form.position === "Executive"}
              onChange={this.onChangePositionValue}/>
                            <Form.Control placeholder="Executive" disabled/>
                          </InputGroup>
                      </td>
                      <td>
                          <InputGroup   style={{width:"150px",padding:"5px"}}>
                            <InputGroup.Radio aria-label="Checkbox for following text input" onChange={this.onChangePositionValue} name="group1"  value="Reviewer" checked = {this.state.add_new_user_form.position === "Reviewer"}/>
                            <Form.Control placeholder="Reviewer" disabled/>
                          </InputGroup>
                      </td>
                    </tr>
                  </center>
                </Form.Group>
              
                <Form.Group className="mb-6">
                  <Form.Label>Allowed Cities</Form.Label>
                  <center>
                    <tr>
                      { Object.entries(this.state.list_of_cities).map(([k,v]) =>
                        <td>
                        <InputGroup  style={{width:"150px",padding:"5px"}}>
                          <InputGroup.Checkbox name="group2" value={k} onChange={this.onChangeCitiesValue} checked={this.state.add_new_user_form.cities[k] }
                          />
                          <Form.Control placeholder={k} disabled/>
                        </InputGroup>
                      </td>
                      )  
                      }
                    </tr>
                  </center>
                </Form.Group>

              </Form>
              
              
              
              <br />
              <center>
                <Button className="btn-primary" style={{width:"150px"}} onClick={this.AddUserData}>Add </Button>
                <Button className="btn-danger" style={{width:"150px"}} onClick={this.reset_add_new_user_model}>Reset </Button>
              </center>
              <br />
            </Modal.Body>

            <Modal.Footer>
              
            </Modal.Footer>
          </Modal>

          {/* Model Box Finsihs */}
        </div>

        <div style={{ width: "100%" }} className="model_box">
          <Modal
            dialogClassName="modal_width_styles"
            contentClassName="modal_height_styles"
            isOpen={this.state.edit_user_model}
            onRequestClose={this.hide_edit_user_model}
            show={this.state.edit_user_model}
            onHide={this.hide_edit_user_model}
            keyboard={false}
            style={{ width: "100%", height: "100%" }}
          >
            <Modal.Header closeButton>
              <Modal.Title>
                User Information
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Form>
              <Form.Group className="mb-2">
                  <Form.Label>User Fullname</Form.Label>
                  <Form.Control
                    value={this.state.edit_user_form.fullname}
                    onChange={(e) => this.onChangeTextField_edit_user(e, "fullname")}

                  />
                </Form.Group>
              <table className="model_table_">
                
              <tr className="model_table_row">
                    <td className="model_table_data">
                <Form.Group className="mb-2">
                  <Form.Label>Username</Form.Label>
                  <Form.Control
                    value={this.state.edit_user_form.username}
                    onChange={(e) => this.onChangeTextField_edit_user(e, "username")}
                  />
                </Form.Group>
                </td>
                <td className="model_table_data">
                <Form.Group className="mb-2">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    value={this.state.edit_user_form.password}
                    onChange={(e) => this.onChangeTextField_edit_user(e, "pwd")}
                  />

                </Form.Group>
                </td>
                </tr>
                </table>
                 
                <Form.Group className="mb-6">
                  <Form.Label>Position</Form.Label>
                  <center>
                    <tr>
                        <td>
                          <InputGroup  style={{width:"150px",padding:"5px"}}>
                            <InputGroup.Radio  value="Executive" name="group1" checked = {this.state.edit_user_form.position === "Executive"}
              onChange={this.onChangePositionValue_edit_user}/>
                            <Form.Control placeholder="Executive" disabled/>
                          </InputGroup>
                      </td>
                      <td>
                          <InputGroup   style={{width:"150px",padding:"5px"}}>
                            <InputGroup.Radio  onChange={this.onChangePositionValue_edit_user} name="group1"  value="Reviewer" checked = {this.state.edit_user_form.position === "Reviewer"}/>
                            <Form.Control placeholder="Reviewer" disabled/>
                          </InputGroup>
                      </td>
                    </tr>
                  </center>
                </Form.Group>
              
                <Form.Group className="mb-6">
                  <Form.Label>Allowed Cities</Form.Label>
                  <center>
                    <tr>
                      { Object.entries(this.state.list_of_cities).map(([k,v]) =>
                        <td>
                        <InputGroup  style={{width:"150px",padding:"5px"}}>
                          <InputGroup.Checkbox name="group2" value={k} onChange={this.onChangeCitiesValue_edit_user}  checked={this.state.edit_user_form.cities[k] }
                          />
                          <Form.Control placeholder={k} disabled/>
                        </InputGroup>
                      </td>
                      )  
                      }
                    </tr>
                  </center>
                </Form.Group>

              </Form>
              
              <br />
              <center>
                <Button className="btn-primary" style={{width:"150px"}} onClick={this.UpdateUserData}>Update </Button>
                
              </center>
              <br />
            </Modal.Body>

            <Modal.Footer>
              
            </Modal.Footer>
          </Modal>

          {/* Model Box Finsihs */}
        </div>
    </div>
  );
  }
}
