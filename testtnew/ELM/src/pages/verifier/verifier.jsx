import React, { Component } from "react";
import TopNavbar from "../global/components/navbar";
import MiniDrawer from "../global/components/Sidebar";
import Card from "react-bootstrap/Card";
import "./index.css";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

export default class Verifier extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show_users: [],
      users:[],
      filter_table: {
        fullname: "",
        position: ""
      }
     }
    this.GetData = this.GetData.bind(this);
    this.apply_filter = this.apply_filter.bind(this);
    this.reset_filter = this.reset_filter.bind(this);
    this.handleChange_fullname = this.handleChange_fullname.bind(this);
    this.handleChange_pos = this.handleChange_pos.bind(this);
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
          show_users: response.data.users
        });
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
  render() {
  return (
    <div>
      <MiniDrawer />
      <TopNavbar />
      <Card className="card_bg" style={{marginLeft:"7%",marginTop:"-5%",paddingRight:"20px",marginRight:"20px"}}>
      <div className="verifier_cases_details_table">
      <h2><u>User Information Table</u></h2>
        
       <br />
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
                    <td>
                      {" "}
                      <Button
                        variant="primary"
                        style={{ height: "60%" }}
                        onClick={() =>{  window.location.href ="/verifier/user/"+x.user_id;  }}
                      >
                        View Details
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
    </div>
  );
  }
}
