import { React, Component } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { useState } from "react";
import { Checkbox } from "@mui/material";
import "./index.css";
import { Button, Modal, Input } from "react-bootstrap";
//import "./index.css";
// import Button from "react-bootstrap/Button";
import ModalMap from "./ModalMap";
import Form from "react-bootstrap/Form";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import Card from "react-bootstrap/Card";

export default class NewTable extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show_model: false,
      status: "Not Reported",
      currentPage: 1,
      data: [],
      render: false,
      model_show_violation_info: {
        violation_id: 0,
        violation_type_id: 0,
        accurate: 0,
        risk: 0,
        display_img: "0",
        violation_date: "JAn 00, 0000",
        violation_time: "00:00",
        violation_name: "",
        lat: 0,
        lng: 0,
        status: "Not Reported",
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
      .get(this.props.server + "/get_single_violation/" + para)
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
          <tr>
            <td>
              <Checkbox />
            </td>
            <td>{O.violation_id}</td>
            <td>
              {O.violation_date} at {O.violation_time}
            </td>
            <td>{O.violation_name}</td>
            <td>{O.accurate}</td>
            <td>{O.risk}</td>
            <td>
              {" "}
              <Button
                variant="primary"
                style={{ height: "60%" }}
                onClick={this.showModal(O.violation_id)}
              >
                Show Details
              </Button>
            </td>
          </tr>
        );
      });
      return rows;
    };

    return (
      // <Card style={{ borderRadius: "3rem", marginTop: "5rem" }}>
      <div className="violation_cases_details_table" >
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
              <tbody>{calll()}</tbody>
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
                <Form.Group className="mb-3">
                  <Form.Label>Risk</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.risk}
                    disabled
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Accurate</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.accurate}
                    disabled
                  />
                </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Label>Current Status</Form.Label>
                  <Form.Control
                    placeholder={this.state.model_show_violation_info.status}
                    disabled
                  />
                </Form.Group>
              </Form>
              <div
                className="violation_action_buttons"
                style={{ marginLeft: "15%", marginTop: "10px" }}
              >
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
              count={this.props.table_data.pages}
              onChange={this.handleChange}
            />
          </Stack>
        </div>
      </div>
      // </Card>
    );
  }
}
