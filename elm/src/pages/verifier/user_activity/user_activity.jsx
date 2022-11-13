import React, { Component } from "react";
import "../../global/style/style.css";
import { Navigate } from "react-router-dom";
import TopNavbar from "../../global/components/navbar";
import MiniDrawer from "../../global/components/Sidebar";
import { Button, Modal, Input } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import ModalMap from "../../violation/ModalMap";
export default class UserActivity extends Component {
  constructor(props) {
    super(props);
    var url = window.location.href;
    var id = url.substring(url.lastIndexOf("/") + 1);
    this.state = {
        user_id: id,
        activity:[],
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
    };
    this.get_user_activity = this.get_user_activity.bind(this);
    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
    this.get_user_activity();
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
  get_user_activity() {
    const com = this;
    const axios = require("axios").default;
    axios.get(this.props.server+"/get_user_activity/"+this.state.user_id).then(function (response) {
      // handle success
      
      com.setState({
        activity: response.data.activity,
        
      });
    });
  }
  render() {
    return(
        <div>
            <MiniDrawer />
            <TopNavbar />
            <div className="verifier_cases_details_table">
                <div class="row">
                <div class="table-responsive ">
            <table class="table table-striped table-hover table-bordered">
              <thead>
                <tr>
                  
                  <th style={{ fontFamily: "Verdana" }}>Log ID</th>
                  <th style={{ fontFamily: "Verdana" }}>Violation ID </th>
                  <th style={{ fontFamily: "Verdana" }}>Prev Violation Type</th>
                  <th style={{ fontFamily: "Verdana" }}>Updated Violation Type</th>
                  <th style={{ fontFamily: "Verdana" }}>Correct/Incorrect</th>
                  <th style={{ fontFamily: "Verdana" }}>Entry Date</th>
                  <th style={{ fontFamily: "Verdana" }}>View</th>
                </tr>
              </thead>
              <tbody>
                {this.state.activity.map((x)=>(
                  <tr>
                  
                  <td>{x.log_id}</td>
                  <td>{x.violation_id}</td>
                  <td>{x.prev_vio}</td>
                  <td>{x.updated_vio}</td>
                  <td>{x.cor}</td>
                  <td>{x.entry_date}</td>
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
        </div>
    );
  }
}