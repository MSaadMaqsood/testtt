import React, { Component } from "react";
import TopNavbar from "../global/components/navbar";
import MiniDrawer from "../global/components/Sidebar";
import Divider from "@mui/material/Divider";
import Card from "react-bootstrap/Card";
import NewTable from "./NewTable";
import "./index.css";

export default class Street extends Component {
  constructor(props) {
    super(props);

    var url = window.location.href;
    var id = url.substring(url.lastIndexOf("/") + 1);
    this.state = {
      total_vioaltions: 0,
      street_id: id,
      street_name: "",
      list_of_vio: [],
      violation_table: { myData: [], pages: 1,vio:[] },
      render: false,
    };

    this.GetData = this.GetData.bind(this);
    this.GetData();
  }

  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(this.props.server + "/get_street_vio_Verify/" + this.state.street_id)
      .then(function (response) {
        com.setState({
          violation_table: response.data,
          total_vioaltions: response.data.myData.length
        });
        
      });
      
  }

  change = (e) => {
    window.location.href = "/violation/" + e.target.value;
  };
  
  render() {
    
    var table_send = () => {
      if (this.state.to_render) {
      }
    };
    return (
      <div >
        <TopNavbar />
        <MiniDrawer />
        <Card className="card_bg" style={{marginLeft:"7%",marginTop:"-5%",paddingRight:"20px",marginRight:"20px"}}>
      <div className="verifier_street_card">

        
      <h3 style={{marginLeft: "20px" ,marginTop:"30px"}}><u>{("UnVerified Violations Table")}</u></h3>
        <h5 style={{ marginLeft: "20px" ,marginTop:"10px"}}>
          Total violations: {this.state.total_vioaltions}
        </h5>
        <Divider className="violation_divider" />
        <NewTable
          table_data={this.state.violation_table}
          ref={this.child}
          changed="true"
          server={this.props.server}
        />

        {/* <Card.Text className="violation_content_card_body_text_subheadings_lasttwo">
          Action
        </Card.Text>
        <Divider className="violation_divider" /> */}
        {/* <div className="violation_action_buttons">
          <button type="button" class="btnn">
            Call Ejadah
          </button>
          <button type="button" class="btnn">
            Call Amanah
          </button>
          <button type="button" class="btnn">
            Call Police
          </button>
        </div> */}
        <Divider className="violation_divider" />
        </div>
        </Card>
      </div>
    );
  }
}
