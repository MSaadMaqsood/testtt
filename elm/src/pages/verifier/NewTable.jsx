import { React, Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { Checkbox } from "@mui/material";
import "./index.css";
import { Button, Modal, Input } from "react-bootstrap";
//import "./index.css";
// import Button from "react-bootstrap/Button";
import ModalMap from "../global/components/ModelMap";
import Form from "react-bootstrap/Form";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import Card from "react-bootstrap/Card";
import InputGroup from 'react-bootstrap/InputGroup';

export default class NewTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show_model: false,
      status: "Not Reported",
      currentPage: 1,
      data: [],
      AI_correct: false,
      render: false,
      show_uploading: false,
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
    };
    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.change = this.change.bind(this);
    this.update_violation_cor = this.update_violation_cor.bind(this);
    this.update_violation_incor = this.update_violation_incor.bind(this);
  }
  showModal = (para) => (e) => {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server + "/get_single_violation_Verify/" + para)
      .then(function (response) {
        com.setState({
          model_show_violation_info: response.data,
          show_model: true,
        });
      });
  };
  update_violation_cor() {
    const com = this;
    const server = this.props.server;
   const axios = require('axios').default;
   this.setState({show_uploading:true});
    axios.post(this.props.server+"/update_violation_for_verify", {'user_id': sessionStorage.getItem("user_id"), 'violation_id': this.state.model_show_violation_info.violation_id, 'prev_vio_id': this.state.model_show_violation_info.violation_type_id, 'updated_vio_id': this.state.model_show_violation_info.new_violation_type_id, 'cor':1})
    .then(function (response) {
      com.setState({show_uploading:false});
      alert("Violation updated! Refresh Page");  
    })
    
  }
  update_violation_incor() {
    const com = this;
    const server = this.props.server;
   const axios = require('axios').default;
    axios.post(this.props.server+"/update_violation_for_verify", {'user_id': sessionStorage.getItem("user_id"), 'violation_id': this.state.model_show_violation_info.violation_id, 'prev_vio_id': this.state.model_show_violation_info.violation_type_id, 'updated_vio_id': this.state.model_show_violation_info.new_violation_type_id, 'cor':0})
    .then(function (response) {
      alert("Violation updated! Refresh Page");  
    })
    
  }
  hideModal = () => {
    this.setState({ show_model: false });
  };
  toggleCorrect = () => {
    this.setState({ AI_correct: true });
    alert("Violation verified");
  };

  handleChange = (e, value) => {
    this.setState({ currentPage: value });
  };
  handleChange_check = (event) => {
    console.log(event.target.value + " " + event.target.checked);
  };

  change = (e) => {
    let temp = this.state.model_show_violation_info;
    temp.new_violation_type_id = e.target.value;
    this.setState({model_show_violation_info : temp}); 
    
  };

  render() {
    
    return (
      // <Card style={{ borderRadius: "3rem", marginTop: "5rem" }}>
      <div className="verifier_cases_details_table_big">
        <div class="row ">
          <div class="col-sm-3 offset-sm-1  mt-5 mb-4 text-gred"></div>
        </div>
        <div class="row">
          <div class="table-responsive ">
            <table class="table table-striped table-hover table-bordered">
              <thead>
                <tr>
                  <th></th>
                  <th style={{ fontFamily: "Verdana" }}>VIOLATION ID</th>
                  <th style={{ fontFamily: "Verdana" }}>DATE & TIME </th>
                  <th style={{ fontFamily: "Verdana" }}>VIOLATION NAME</th>
                  <th style={{ fontFamily: "Verdana" }}>ACCURACY </th>
                  <th style={{ fontFamily: "Verdana" }}>RISK </th>
                  <th style={{ fontFamily: "Verdana" }}>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                {this.props.table_data.myData.map((x)=>(
                  <tr>
                  <td>
                    <Checkbox />
                  </td>
                  <td>{x.violation_id}</td>
                  <td>{x.violation_date} at {x.violation_time}</td>
                  <td>{x.violation_name}</td>
                  <td>{x.accurate}</td>
                  <td>{x.risk}</td>
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
                )

                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* <!--- Model Box ---> */}
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
              <table className="model_table_">
                  <tr className="model_table_row">
                    <td className="model_table_data">
                    <Form.Group className="mb-3">
                  <Form.Label>Violation Type</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.violation_name}
                    disabled
                  />
                </Form.Group>
                    </td>
                    <td>
                    <Form.Group className="mb-3">
              <Form.Label>Change to</Form.Label>
                 <Form.Select 
                  class="violation_select"
                  aria-label="Default select example"
                  onChange={this.change}
                  
                >
                  <option value={this.state.model_show_violation_info.violation_type_id}>{this.state.model_show_violation_info.violation_name}</option>
                  {
                    this.props.table_data.vio.map((h)=>(
                      <option value={h.vio_id}>{h.name}</option>
                    ))
                  } 
                </Form.Select>
                
               
                </Form.Group>
                    </td>
                  </tr>
                </table>
              
                
                <table className="model_table_">
                  <tr className="model_table_row">
                    <td style={{width:"33%"}}>
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
                    </td>
                    <td  style={{width:"33%"}}>
                    <Form.Group className="mb-3">
                  <Form.Label>Risk</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.risk}
                    disabled
                  />
                </Form.Group>
                    </td>
                    <td   style={{width:"33%"}}>
                    <Form.Group className="mb-3">
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
              <div
              style={{ marginLeft: "40%", marginTop: "10px" }}
              >
                <label>{this.state.show_uploading && "Updating Wait......"}</label>
              </div>
              <div
                className="verifier_action_buttons"
                style={{ marginLeft: "35%", marginTop: "10px" }}
              >
                <button type="button" class="btnn" onClick={this.update_violation_cor}>
                  Correct
                </button>
                <button type="button" class="btnn" onClick={this.update_violation_incor}>
                  Incorrect
                </button>
              </div>
              <div className="Modal_verifier">
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

            <Modal.Footer onClick={this.hideModal}></Modal.Footer>
          </Modal>

          {/* Model Box Finsihs */}
        </div>
        {/* <div className="pagination_style">
          <Stack spacing={2}>
            <Pagination
              count={this.props.table_data.pages}
              onChange={this.handleChange}
            />
          </Stack>
        </div> */}
      </div>
      // </Card>
    );
  }
}
