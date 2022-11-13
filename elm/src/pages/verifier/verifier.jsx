import React, { Component } from "react";
import TopNavbar from "../global/components/navbar";
import MiniDrawer from "../global/components/Sidebar";
import "./index.css";
import { useNavigate } from "react-router-dom";
import { Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

export default class Verifier extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    }
    this.GetData = this.GetData.bind(this);
    this.GetData();
  }
  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server + "/get_vio_for_verify")
      .then(function (response) {
        com.setState({
          data: response.data.streets,
          
        });
      });
  }
  
  render() {
  return (
    <div>
      <MiniDrawer />
      <TopNavbar />
      <div className="verifier_cases_details_table">
        <div class="row">
          <div class="verifier-table-responsive ">
            <table class="table table-striped table-hover table-bordered">
              <thead>
                <tr>
                  <th style={{ fontFamily: "Verdana" }}>STREET NAME</th>
                  <th style={{ fontFamily: "Verdana" }}>
                    NUM OF UNREPORTED VIOLATIONS{" "}
                  </th>
                  <th style={{ fontFamily: "Verdana" }}></th>
                </tr>
              </thead>
              <tbody>
                {
                  this.state.data.map((x)=>(
                    <tr>
                    <td>{x.name}</td>
                    <td>{x.count}</td>
  
                    <td>
                      {" "}
                      <Button
                        variant="primary"
                        style={{ height: "60%" }}
                        onClick={() =>{  window.location.href ="/verifier/street/"+x.streetid;  }}
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
    </div>
  );
  }
}
