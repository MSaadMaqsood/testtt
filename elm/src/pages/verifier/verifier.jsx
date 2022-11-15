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
      data: [],
      users:[],
      show_streets: false
    }
    this.GetData = this.GetData.bind(this);
    this.Show_user = this.Show_user.bind(this);
    this.Show_street = this.Show_street.bind(this);
    this.GetData();
  }
  Show_user(){
    this.setState({show_streets: false});
  }
  Show_street(){
    this.setState({show_streets: true});
  }
  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server + "/get_vio_for_verify")
      .then(function (response) {
        com.setState({
          data: response.data.streets,
          users: response.data.users
          
        });
      });
  }
  
  render() {
  return (
    <div>
      <MiniDrawer />
      <TopNavbar />
      <Card className="card_bg" style={{marginLeft:"7%",marginTop:"-5%",paddingRight:"20px",marginRight:"20px"}}>
      <div className="verifier_cases_details_table">
      <h2><u>{!this.state.show_streets && ("User Information Table")}</u></h2>
      <h2><u>{this.state.show_streets && ("Streets UnVerified Violations Table")}</u></h2>
        <div style={{ paddingBottom:"30px",paddingRight:"30px" }}>
        {
              this.state.show_streets && ( <Button
                        variant="primary"
                        style={{ height: "60%",float:"right"}}
                        onClick={this.Show_user}
                      >
                        View Users
      </Button>
              )}
              {
              !this.state.show_streets && (
      <Button
                        variant="primary"
                        style={{ height: "60%",float:"right"}}
                        onClick={this.Show_street}
                      >
                        View Streets
      </Button>
              )}
      </div>
      <br />
        <div class="row">
        
          <div class="verifier-table-responsive " style={{ paddingBottom:"15px",paddingRight:"25px" }}>
            {
              this.state.show_streets && (<table class="table table-striped table-hover table-bordered">
              <thead>
                <tr>
                  <th style={{ fontFamily: "Verdana" }}>Street Name</th>
                  <th style={{ fontFamily: "Verdana" }}>
                    Count of Unverified Violations{" "}
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
            </table>)
            }
            {
              !this.state.show_streets && (<table class="table table-striped table-hover table-bordered">
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
                  this.state.users.map((x)=>(
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
            </table>)
            }
          </div>
        </div>
      </div>
      </Card>
    </div>
  );
  }
}
