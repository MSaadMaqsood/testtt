import PropTypes from "prop-types";
import React, { Component } from "react";
import { Switch } from "@mui/material";
import Modal from "react-modal";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { XOctagon} from "react-bootstrap-icons";
import ModalMap from "./ModalMap";
export default class Table extends Component {
  constructor(props) {
    super(props);
    this.state = {
      total_violations: 6,
      show_img: false,
      status: "Not Reported",
      imgPathToShow: "",
      countPages: 3,
      currentPage: 1,
      data: [],
      render: false,
      tabledata: [
        {
          "violation_id": 1,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 2,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 3,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 4,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 5,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 6,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 7,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 8,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 9,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 10,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 11,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 12,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
        {
          "violation_id": 13,
          "violation_type_id": 1,
          "accurate": 90,
          "risk": 10,
          "display_img": "1.jpg",
          "violation_date": "June 10, 2022",
          "violation_time": "13:05",
          "violation_name": "Asphalt"
        },
      ],
    };
    this.showModal_img = this.showModal_img.bind(this);
    this.hideModal_img = this.hideModal_img.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.GetData = this.GetData.bind(this);
    
    this.componentDidMount();
  }

  showModal_img = (para) => (e) => {
    this.setState({ show_img: true, imgPathToShow: para });
  };
  changeStatus = () => {
    this.setState({ status: "Reported" });
  };
  hideModal_img = () => {
    this.setState({ show_img: false, imgPathToShow: "" });
  };

  handleChange = (e, value) => {
    this.setState({ currentPage: value });
  };

  handleChange_check = (event) => {
    console.log(event.target.value + " " + event.target.checked);
  };

  componentDidMount() {
    setTimeout(
      function () {
        this.setState({ render: true });
      }.bind(this),
      2000
    );
  }

  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get("http://67.205.163.34:1159/get_violations/1")
      .then(function (response) {
        // handle success

        com.setState({
          data: response.data.myData,
          countPages: response.data.pages,
        });
      });
  }

  render() {
    const calll = () => {
      const hh = this.state.tabledata.slice(
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
                onClick={this.showModal_img(
                  "http://67.205.163.34:1159/showviolationimage/" +
                    O.display_img
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
          isOpen={this.state.show_img}
          onRequestClose={this.hideModal_img}
          contentLabel="Example Modal"
          className="violation_cases_details_table_model"
        >
          <br />
         
          <XOctagon onClick={this.hideModal_img} style={{ float: "right", height:"30px", width:"30px" }}  />
          <br />
          <br />
          <div className="Modal_violation">
            <img
              src={this.state.imgPathToShow}
              style={{ width: "50%", height: "300px" }}
            />
            <div className="map_size">
              <ModalMap />
            </div>
          </div>
          <div className="row_of_modal">
            <div class="row row_col" style={{marginTop: "10px"}}>
              <table>
                <tr>
                  <td>Date Time:</td>
                  <td>Sep 24, 2022 at 13:14</td>
                </tr>
                <tr>
                  <td>Violation Type:</td>
                  <td>Asphalt</td>
                </tr>
                <tr>
                  <td>Accurate:</td>
                  <td>90%</td>
                </tr>
                <tr>
                  <td style={{color:"red"}}>Risk:</td>
                  <td  style={{color:"red"}}>10%</td>
                </tr>
              </table>  
            </div>
              <div className="row_col">
            <h6 className="violation_modal_current_status" style={{marginTop:"10px"}}>
              Current Status: {this.state.status}
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
              count={3}
              onChange={this.handleChange}
            />
          </Stack>
        </div>
      </div>
    );
  }
}
