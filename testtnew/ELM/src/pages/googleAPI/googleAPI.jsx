import React, { Component } from "react";
import "../global/style/style.css";
import TopNavbar from "../global/components/navbar";
import MiniDrawer from "../global/components/Sidebar";
import { Navigate } from "react-router-dom";
import "./googleAPI.css";
import Card from "react-bootstrap/Card";

export default class Google_Api extends Component {
  constructor(props) {
    super(props);
    this.state = {
      currentAPI: "",
      currentcomment: "",
      API: "",
      comments: "",
      go: false,
    };
    this.addAPI = this.addAPI.bind(this);
    this.onChange = this.onChange.bind(this);
    this.GetData = this.GetData.bind(this);
    this.GetData();
  }

  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios.get(this.props.server+"/get_map_api").then(function (response) {
      // handle success

      com.setState({
        currentAPI: response.data.api,
        currentcomment: response.data.comment,
      });
    });
  }
  addAPI() {
    const com = this;
    const server = this.props.server;
   const axios = require('axios').default;
    axios.post(this.props.server+"/insertmapapi", {'api': this.state.API, 'comment': this.state.comments, 'userid':sessionStorage.getItem("user_id")})
    .then(function (response) {
      com.setState({ go: true });  
    })
    
  }
  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  render() {
    if (this.state.go) {
      alert("API Submitted! Refresh Page");
    }
    return (
      <div>
        <MiniDrawer />
        <TopNavbar />
        <div id="api" style={{ marginTop: "-10rem" }}>
          {/* <img class="logo_style" src={logo}></img> */}
          <div class="container">
            <div
              id="api-row"
              class="row justify-content-center align-items-center"
            >
              <div id="api-column" class="col-md-6">
                <div id="api-box" class="col-md-12">
                  <form id="api-form" class="form">
                    <center>
                      {" "}
                      <h2> Google API Details</h2>
                      <hr />
                      <h5> Current API:</h5>
                      <input
                        type="text"
                        name="API"
                        value={this.state.currentAPI}
                        id="API"
                        class="form-control input_txt"
                        disabled
                      />
                      <br />
                      <label for="comments" class="label">
                        Enter any comments:
                      </label>
                      
                      <input
                        type="text"
                        name="API"
                        value={this.state.currentcomment}
                        id="API"
                        class="form-control input_txt"
                        disabled
                      />
                    </center>

                    <hr />
                    <div class="form-group">
                      <label for="comments" class="label">
                        Enter any comments:
                      </label>

                      <br />
                      <input
                        type="text"
                        name="comments"
                        value={this.state.comments}
                        onChange={this.onChange}
                        id="comments"
                        class="form-control input_txt"
                        placeholder="Enter any comments you wish to add"
                      />
                    </div>
                    <div class="form-group">
                      <label for="API" class="label">
                        Enter a new API:
                      </label>
                      <br />
                      <input
                        type="text"
                        name="API"
                        value={this.state.API}
                        onChange={this.onChange}
                        id="API"
                        class="form-control input_txt"
                        placeholder="Enter new API here"
                      />
                    </div>

                    <div class="form-group btn_section">
                      <div class="v-center">
                        <input
                          type="button"
                          name="Submit"
                          class="btn btn-md api_btn"
                          value="Submit"
                          onClick={this.addAPI}
                        />
                      </div>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
