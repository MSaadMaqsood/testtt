import React, { Component } from "react";
import "../global/style/style.css";
import TopNavbar from "./Navbar_login";
import { Navigate } from "react-router-dom";
import "./login.css";
import Card from "react-bootstrap/Card";

export default class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      map_api:"",
      go: false,
    };
    this.login = this.login.bind(this);
    this.onChange = this.onChange.bind(this);
    this.get_map_api = this.get_map_api.bind(this);
    this.get_map_api();
  }
  get_map_api() {
    const com = this;
    const axios = require("axios").default;
    axios.get(this.props.server+"/get_map_api").then(function (response) {
      // handle success
      
      com.setState({
        map_api: response.data.api,
        
      });
    });
  }
  login() {
    if(this.state.map_api === ""){
      alert("No Map Api Found!");
    }else{
      sessionStorage.setItem("user_id", 1);
      sessionStorage.setItem("map_api", this.state.map_api);
      this.setState({ go: true });
    }
  }
  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }
  render() {
    if (this.state.go) {
      return <Navigate to="/Dashboard" />;
    }
    return (
      <div>
        <TopNavbar />
        <div id="login">
          {/* <img class="logo_style" src={logo}></img> */}
          <div class="container">
            <div
              id="login-row"
              class="row justify-content-center align-items-center"
            >
              <div id="login-column" class="col-md-6">
                <div id="login-box" class="col-md-12">
                  <form id="login-form" class="form">
                    <center>
                      {" "}
                      <h2> Login</h2>
                    </center>
                    <hr />
                    <div class="form-group">
                      <label for="username" class="label">
                        Username:
                      </label>
                      <br />
                      <input
                        type="text"
                        name="username"
                        value={this.state.username}
                        onChange={this.onChange}
                        id="username"
                        class="form-control input_txt"
                        placeholder="Enter username here"
                      />
                    </div>
                    <div class="form-group">
                      <label for="landmark" class="label">
                        Password:
                      </label>
                      <br />
                      <input
                        type="text"
                        name="password"
                        id="password"
                        class="form-control input_txt"
                        value={this.state.password}
                        onChange={this.onChange}
                        placeholder="Enter password here"
                      />
                    </div>

                    <div class="form-group btn_section">
                      <div class="v-center">
                        <input
                          type="submit"
                          name="Login"
                          class="btn btn-md login_btn"
                          value="Login"
                          onClick={this.login}
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
