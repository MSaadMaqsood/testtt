import PropTypes from "prop-types";
import React, { Component } from "react";
import { Switch } from "@mui/material";
import Modal from "react-modal";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { XOctagon} from "react-bootstrap-icons";
import ModalMap from "../global/components/ModelMap";

export default class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show_model: false,
      status: "Not Reported",
      currentPage: 1,
      data: [],
      render: false,
      model_show_violation_info: {
        "violation_id": 0,
        "violation_type_id": 0,
        "accurate": 0,
        "risk": 0,
        "display_img": "0",
        "violation_date": "JAn 00, 0000",
        "violation_time": "00:00",
        "violation_name": "",
        "lat": 0,
        "lng": 0,
        "status": "Not Reported"
    },
    };
    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
    this.handleChange = this.handleChange.bind(this);
    
  }
  showModal = (para) => (e) => {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server+"/get_single_violation/"+para)
      .then(function (response) {
        com.setState({
          model_show_violation_info: response.data,
          show_model: true
        });
      });
  };
  changeStatus = () => {
    this.setState({ status: "Reported" });
  };
  hideModal = () => {
    this.setState({ show_model: false });
  };

  handleChange = (e, value) => {
    this.setState({ currentPage: value });
  };
  handleChange_check = (event) => {
    console.log(event.target.value + " " + event.target.checked);
  };

  
  render() {
    const calll = () => {
      const hh = this.props.table_data.myData.slice(
        (this.state.currentPage - 1) * 5,
        (this.state.currentPage - 1) * 5 + 5
      );
      const rows = hh.map((O) => {
        return (
          <div class="row">
            <div class="col-md-auto violation_cases_details_table_row_index">
              <div class="violation_column_cell_serial">{O.violation_id}#</div>
            </div>
            <div class="col">
              <div class="violation_column_cell">
                {O.violation_date + " at " + O.violation_time}
              </div>
            </div>
            <div class="col">
              <div class="violation_column_cell">{O.violation_name}</div>
            </div>
            <div class="col">
              <div class="violation_column_cell">Accurate: {O.accurate}%</div>
            </div>
            <div class="col">
              <div class="violation_column_cell_red">
                <p class="text-danger">Risk: {O.risk}%</p>
              </div>
            </div>
            <div class="col">
              <button
                type="button"
                onClick={this.showModal(
                  O.violation_id
                )}
                class="violation_btn_show_issue"
              >
                Show Details
              </button>
            </div>
            <div class="col">
              <Switch
                value={O.violation_id}
                onChange={this.handleChange_check}
              />
            </div>
          </div>
        );
      });
      return rows;
    };
    return (
      <div style={{marginTop:"10px"}}>
        <hr />
        {calll()}
        <hr />
        <Modal
          isOpen={this.state.show_model}
          onRequestClose={this.hideModal}
          contentLabel="Example Modal"
          className="violation_cases_details_table_model"
        >
          <br />
         
          <XOctagon onClick={this.hideModal} style={{ float: "right", height:"30px", width:"30px" }}  />
          <br />
          <br />
          <div className="Modal_violation">
            <img
              src={this.props.server+'/show_violation_image/'+this.state.model_show_violation_info.display_img}
              style={{ width: "50%", height: "300px" }}
            />
            <div className="map_size">
              <ModalMap latlng={ { lat: this.state.model_show_violation_info.lat , lng: this.state.model_show_violation_info.lng } } />
            </div>
          </div>
          <div className="row_of_modal">
            <div class="row row_col" style={{marginTop: "10px"}}>
              <table>
                <tr>
                  <td>Date Time:</td>
                  <td>{this.state.model_show_violation_info.violation_date} at {this.state.model_show_violation_info.violation_time}</td>
                </tr>
                <tr>
                  <td>Violation Type:</td>
                  <td>{this.state.model_show_violation_info.violation_name}</td>
                </tr>
                <tr>
                  <td>Accurate:</td>
                  <td>{this.state.model_show_violation_info.accurate}%</td>
                </tr>
                <tr>
                  <td style={{color:"red"}}>Risk:</td>
                  <td  style={{color:"red"}}>{this.state.model_show_violation_info.risk}%</td>
                </tr>
              </table>  
            </div>
              <div className="row_col">
            <h6 className="violation_modal_current_status" style={{marginTop:"10px"}}>
              Current Status: {this.state.model_show_violation_info.status}
            </h6>
            <div className="violation_action_buttons" style={{marginLeft: "15%",marginTop:"10px"}}>
                        <button type="button" class="btnn">
                          Call Ejadah
                        </button>
                        <button type="button" class="btnn">
                          Call Amanah
                        </button>
                        <button type="button" class="btnn">
                          Call Police
                        </button>
                      </div>
            </div>
          </div>
          
          
        </Modal>
        <div className="pagination_style">
          <Stack spacing={2}>
            <Pagination
              count={this.props.table_data.pages}
              onChange={this.handleChange}
            />
          </Stack>
        </div>
      </div>
    );
  }
}
