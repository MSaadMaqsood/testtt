import React, { Component } from "react";
import "../global/style/style.css";
import { Navigate } from "react-router-dom";
import TopNavbar from "../global/components/navbar";
import MiniDrawer from "../global/components/Sidebar";
import { Button, Modal, Input } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import ModalMap from "../violation/ModalMap";
import { Pages } from "@material-ui/icons";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";

export default class AllViolations extends Component {
  constructor(props) {
    super(props);
   
    this.state = {
        all_data: [],
        all_pages: 0,
        show_data: [],
        show_pages: 0,
        currentPage:1,
        vio_type_list:[{"name":"000000"}],
        show_model: false,
        model_show_violation_info: {
            violation_id: 1,
            violation_type_id: 2,
            new_violation_type_id: 2,
            accurate: 90,
            risk: 40,
            display_img: "0",
            violation_date: "JAn 00, 0000",
            violation_time: "00:00",
            violation_name: "Rubble",
            lat: 0,
            lng: 0,
            status: "Not Reported",
          },
          filter_table: {
            violation_type: -5,
            device_id: "",
            Correct:""
          }
    };
    this.get_all_violations = this.get_all_violations.bind(this);
    this.show_filter = this.show_filter.bind(this);
    this.clear_filter = this.clear_filter.bind(this);
    this.change_violation_type = this.change_violation_type.bind(this);
    this.change_correct_type = this.change_correct_type.bind(this);
    this.handleChange_devid = this.handleChange_devid.bind(this);
    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
    this.get_all_violations();
  }
  showModal = (para) => (e) => {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server +  "/get_single_violation/" + para)
      .then(function (response) {
        com.setState({
          model_show_violation_info: response.data,
          show_model: true,
        });
      });
  };
  hideModal = () => {
    this.setState({ show_model: false });
  };
  handleChange_P = (e, value) => {
    this.setState({ currentPage: value });
  };
  get_all_violations() {
    const com = this;
    const axios = require("axios").default;
    axios.get(this.props.server+"/get_all_violation").then(function (response) {
      
      com.setState({
        all_data: response.data.myData,
        all_pages:  response.data.pages,
        show_data: response.data.myData,
        show_pages: response.data.pages,
        vio_type_list: response.data.vio
      });
      
    });
  }

  show_filter(){
    
    let filter_data = [];
    if (this.state.filter_table.violation_type == -5){
        filter_data = this.state.all_data;
    }else{
        this.state.all_data.forEach(element => {
            if(element.violation_type_id == this.state.filter_table.violation_type){
                filter_data.push(element);
            }
        });
    }
    if (this.state.filter_table.device_id == ""){
    }else{
        let tempx = [];
        filter_data.forEach(element => {
            if(element.dev_id == this.state.filter_table.device_id){
                tempx.push(element);
            }
        });
        filter_data = tempx;
    }

    if (this.state.filter_table.Correct == ""){
    }else{
        let tempx = [];
        filter_data.forEach(element => {
            if(element.cor == this.state.filter_table.Correct){
                tempx.push(element);
            }
        });
        filter_data = tempx;
    }
var cpages = Math.floor((filter_data.length) / 10);
if ((filter_data.length) % 10 == 0){

}else{
    cpages = cpages + 1
}
this.setState({
    show_data: filter_data,
    show_pages: cpages,
    currentPage:1
});
  }

  clear_filter(){
    const data = this.state.all_data;
    const pages = this.state.all_pages;

    this.setState({
        show_data:data,
        show_pages: pages,
        currentPage:1,
        filter_table: {
            violation_type: -5,
            device_id: "",
            Correct:""
          }
    })
  }
  change_violation_type = (e) => {
    let xx= this.state.filter_table;
    xx.violation_type = parseInt(e.target.value);
    this.setState({
        filter_table:xx
    }); 
    
  };
  change_correct_type=(e)=>{
    let xx= this.state.filter_table;
    xx.Correct = e.target.value;
    this.setState({
        filter_table:xx
    }); 
  };
  handleChange_devid(e){
    let xx= this.state.filter_table;
    xx.device_id = e.target.value;
    this.setState({
        filter_table:xx
    }); 
  }
  render() {
    const calll = () => {
        const hh =this.state.show_data.slice(
          (this.state.currentPage - 1) * 10,
          (this.state.currentPage - 1) * 10 + 10
        );
        console.log(this.state.show_data);
        console.log(hh);
        const rows = hh.map((x) => {
          return (
            <tr>
                  
            <td>{x.violation_id}</td>
            <td>{x.violation_name}</td>
            <td>{x.accurate}</td>
            <td>{x.risk}</td>
            <td>{x.violation_date} at {x.violation_time}</td>
            <td>{x.cor}</td>
            <td>{x.dev_id}</td>
            <td>
              {" "}
              <Button
                variant="primary"
                style={{ height: "60%" }}
                onClick={this.showModal(x.violation_id)}
              >
                Show Details
              </Button>
            </td>
          </tr>
          );
        });
        return rows;
      };
  
    return(
        <div>
            <MiniDrawer />
            <TopNavbar />
            <div className="verifier_cases_details_table">
            
            <div style={{display:"flex",flexDirection:"row", paddingRight:"50px"}}>
            <div class="input-group mb-3" style={{width:"900px"}}>
                <span class="input-group-text" id="basic-addon1">Violation Type </span>
                <select class="form-select" aria-label="Default select example" onChange={this.change_violation_type} >
                    <option value="-5"></option>
                    {this.state.vio_type_list.map((O) => ( <option value={O.vio_id}>{O.name}</option> ))} 
                </select>
            </div>
            
            <div class="input-group mb-3"  style={{width:"900px",marginLeft:"10px"}}>
                <span class="input-group-text" id="basic-addon1">Correct status </span>
                <select class="form-select" aria-label="Default select example" onChange={this.change_correct_type} >
                    <option value=""></option>
                    <option value="Correct">Correct</option>
                    <option value="Incorrect">Incorrect</option>
                    <option value="Pending">Pending</option>
                </select>
            </div>
            <div class="input-group mb-3"  style={{width:"900px",marginLeft:"10px"}}>
                <span class="input-group-text" id="basic-addon1">Device ID: </span>
                <input type="text" class="form-control" value={this.state.filter_table.device_id} onChange={this.handleChange_devid} />
            </div>
            
            <button type="button" class="btn btn-primary mb-3"  onClick={this.show_filter}  style={{width:"400px"}}>Filter </button>
            <button type="button" class="btn btn-danger mb-3"  onClick={this.clear_filter}  style={{width:"400px"}}>Reset Filter </button>
            </div>
                <div class="row" style={{paddingRight:"50px"}}>
                <div class="table-responsive ">
                
            <table class="table table-striped ">
              <thead>
                <tr>
                  
                  
                  <th style={{ fontFamily: "Verdana" }}>Violation ID </th>
                  <th style={{ fontFamily: "Verdana" }}>Type </th>
                  <th style={{ fontFamily: "Verdana" }}>Accuracy</th>
                  <th style={{ fontFamily: "Verdana" }}>Risk</th>
                  <th style={{ fontFamily: "Verdana" }}>Date && Time</th>
                  <th style={{ fontFamily: "Verdana" }}>Correct/Incorrect</th>
                  <th style={{ fontFamily: "Verdana" }}>Device ID</th>
                    <th></th>
                
                </tr>
              </thead>
              <tbody>
              {calll()}
              </tbody>
            </table>
          </div>
                </div>
            </div>
            <div style={{ width: "100%" }} className="model_box">
          <Modal
            dialogClassName="modal_width_styles"
            contentClassName="modal_height_styles"
            isOpen={this.state.show_model}
            onRequestClose={this.hideModal}
            show={this.state.show_model}
            onHide={this.hideModal}
            keyboard={false}
            style={{ width: "100%", height: "100%" }}
          >
            <Modal.Header closeButton>
              <Modal.Title>
                Violation #{this.state.model_show_violation_info.violation_id}{" "}
                Details
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Violation Type</Form.Label>
                  <Form.Control
                    placeholder={
                      this.state.model_show_violation_info.violation_name
                    }
                    disabled
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Date & Time</Form.Label>
                  <Form.Control
                    placeholder={
                      this.state.model_show_violation_info.violation_date +
                      " at " +
                      this.state.model_show_violation_info.violation_time
                    }
                    disabled
                  />
                </Form.Group>
                <table className="model_table_">
                  <tr className="model_table_row">
                    <td className="model_table_data">
                    <Form.Group className="mb-4">
                  <Form.Label>Risk</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.risk}
                    disabled
                  />
                </Form.Group>
                    </td>
                    <td>
                    <Form.Group className="mb-4">
                  <Form.Label>Accurate</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.accurate}
                    disabled
                  />
                </Form.Group>
                    </td>
                  </tr>
                </table>
                
              </Form>
              
              <div className="Modal_violation">
                <img
                  src={
                    this.props.server +
                    "/show_violation_image/" +
                    this.state.model_show_violation_info.display_img
                  }
                  style={{
                    width: "45%",
                    height: "60%",
                    paddingTop: "5%",
                    marginLeft: "2%",
                  }}
                />
                <div
                  className="map_size"
                  style={{
                    width: "10%",
                    minWidth: "10%",
                    height: "40%",
                    paddingTop: "2%",
                    float: "right",
                    marginRight: "30%",
                    paddingBottom: "5%",
                  }}
                >
                  <ModalMap
                    latlng={{
                      lat: this.state.model_show_violation_info.lat,
                      lng: this.state.model_show_violation_info.lng,
                    }}
                  />
                </div>
              </div>

              {/* 
            <img
              src={
                "http://67.205.163.34:2626/show_violation_image/" +
                this.state.model_show_violation_info.display_img
              }
              style={{ width: "50%", height: "300px" }}
            /> */}

              <br />
              <br />
            </Modal.Body>

            <Modal.Footer  onClick={this.hideModal}>
              
            </Modal.Footer>
          </Modal>

          {/* Model Box Finsihs */}
        </div>
        <div className="pagination_style">
          <Stack spacing={2}>
            <Pagination
              count={this.state.show_pages}
              onChange={this.handleChange_P}
            />
          </Stack>
        </div>
        </div>
    );
  }
}