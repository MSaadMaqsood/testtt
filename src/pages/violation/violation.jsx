import { React, Component } from "react";
import "../global/style/style.css";
import TopNavbar from "../global/components/navbar";
import MiniDrawer from "../global/components/Sidebar";
import Collapsible from "react-collapsible";
import Card from "react-bootstrap/Card";
import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import ExpandCircleDownIcon from "@mui/icons-material/ExpandCircleDown";
import Table from "./Table";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import { Link, useParams } from "react-router-dom";

class Violation extends Component {
  constructor(props) {
    super(props);
    var url = window.location.href;
    var id = url.substring(url.lastIndexOf("/") + 1);
    this.state = {
      total_vioaltions: 13,
      street_id: id,
      render: false,
      list_of_streets: [
        {"street_id": 1, "street_name": "Street_1"},
        {"street_id": 2, "street_name": "Street_2"},
        {"street_id": 3, "street_name": "Street_3"},
    ],
      data:[
          {"street_id": 1, "street_name": "Street_1", "street_risk_rate": 15, "green_index": 85, "Asphalt": 40, "Sidewalk": 60, "Lighting": 71, "Cleanliness": 90, "Afforestation": 95, "Fossils": 92},
          {"street_id": 2, "street_name": "Street_2", "street_risk_rate": 5, "green_index": 95, "Asphalt": 60, "Sidewalk": 75, "Lighting": 99, "Cleanliness": 92, "Afforestation": 92, "Fossils": 87},
          {"street_id": 3, "street_name": "Street_3", "street_risk_rate": 8, "green_index": 92, "Asphalt": 85, "Sidewalk": 49, "Lighting": 65, "Cleanliness": 82, "Afforestation": 77, "Fossils": 55}
        ],
        selected_street: 0
      };

    this.GetData = this.GetData.bind(this);
    this.componentDidMount = this.componentDidMount.bind(this);
    this.setter = this.setter.bind(this);
    this.selected = {}
    for (var i of this.state.data){
      if(i.street_id == this.state.street_id){
        const vv = {"street": {"street_id": i.street_id, "street_name": i.street_name, "street_risk_rate": i.street_risk_rate, "green_index": i.green_index}, 
        "street_health": {"Asphalt": i.Asphalt, "Sidewalk": i.Sidewalk, "Lighting": i.Lighting, "Cleanliness": i.Cleanliness, "Afforestation": i.Afforestation, "Fossils": i.Fossils}
      }
      this.selected = vv;
      }
    }
    console.log(this.selected)
    this.componentDidMount();
  }
  componentDidMount() {
    setTimeout(
      function () {
        this.setState({ render: true });
      }.bind(this),
      500
    );
  }
  setter(){
   

  }
  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(
        "http://67.205.163.34:1159/get_violation_page/" + this.state.street_id
      )
      .then(function (response) {
        // handle success

        com.setState({
          data: response.data,
          list_of_streets: response.data.list_of_streets,
        });
      });
  }
  change = (e) => {
    window.location.href = "/violation/" + e.target.value;
  };

  render() {
    
    
    const get_streets = this.state.list_of_streets.map((O) => {
      return <option value={O.street_id}>{O.street_name}</option>;
    });

   

    return (
      <div>
        <MiniDrawer />
        <TopNavbar />

        <div className="violation_container">
          <div className="violation_content_cards">
            <Card className="violation_content_card_main">
              <Card.Body className="violation_content_card_body">
                <Card.Title className="violation_content_card_body_title">
                  Street Health
                </Card.Title>
                <Card.Title className="violation_content_card_body_title_right">
                  Risk Rate:{" "}
                  {this.selected.street.street_risk_rate}
                  %
                </Card.Title>
                <Card.Text className="violation_content_card_body_text">
                  These cases related to{" "}
                  {this.selected.street.street_name}{" "}
                  street
                </Card.Text>
                <Box
                  sx={{
                    width: this.state.render
                      ? (this.selected.street.green_index / 3).toString() +
                        "%"
                      : "0",
                    height: 20,
                    backgroundColor: "#00c04b",
                    marginTop: "-10px",
                  }}
                />

                <Divider className="violation_divider" />
                <select
                  class="violation_select"
                  aria-label="Default select example"
                  onChange={this.change}
                >
                  <option value={this.selected.street.street_id}>{this.selected.street.street_name}</option>
                  {get_streets}
                </select>

                <Card.Text className="violation_content_card_body_text_subheadings_lastone">
                  Street Status
                </Card.Text>

                <Divider className="violation_divider" />

                <div className="violation_content_cards_statuses">
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Asphalt Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.selected.street_health.Asphalt.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.selected.street_health.Asphalt > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.selected.street_health.Asphalt >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "4px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.selected.street_health.Asphalt}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Sidewalk Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.selected.street_health.Sidewalk.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.selected.street_health.Sidewalk > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.selected.street_health.Sidewalk >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "4px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.selected.street_health.Sidewalk}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Lighting Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.selected.street_health.Lighting.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.selected.street_health.Lighting > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.selected.street_health.Lighting >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "4px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.selected.street_health.Lighting}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Cleanliness Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.selected.street_health.Cleanliness.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.selected.street_health.Cleanliness > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.selected.street_health.Cleanliness >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "4px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.selected.street_health.Cleanliness}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Afforestation Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.selected.street_health.Afforestation.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.selected.street_health.Afforestation > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.selected.street_health.Afforestation >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "4px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.selected.street_health.Afforestation}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Fossils Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.selected.street_health.Fossils.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.selected.street_health.Fossils > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.selected.street_health.Fossils >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "4px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.selected.street_health.Fossils}
                        %
                      </p>
                    </Box>
                  </Card>
                </div>
                <div>
                  <Box
                    sx={{
                      width: this.state.render
                        ? this.selected.street.green_index.toString() + "%"
                        : "0",
                      height: 25,
                      backgroundColor: "#00c04b",
                      marginTop: "15px",
                      float: "left",
                    }}
                  >
                    <p className="GreenIndex">
                      Green Index:{" "}
                      {this.state.render && this.selected.street.green_index}%
                    </p>
                  </Box>
                  <Box
                    sx={{
                      width: this.state.render
                        ? (
                            100 - this.selected.street.green_index
                          ).toString() + "%"
                        : "0",
                      height: 25,
                      backgroundColor:
                        this.state.render &&
                        this.selected.street.green_index >= 50
                          ? "orange"
                          : "red",
                      marginTop: "15px",
                      float: "left",
                    }}
                  ></Box>
                  <br />
                  <br />
                  <hr />
                  <Card.Text className="violation_content_card_body_text_subheadings_firstone">
                    Cases Details
                  </Card.Text>
                  <Collapsible trigger={<ExpandCircleDownIcon />}>
                    <Divider className="violation_divider" />

                    <h6 className="violation_cases_deatils_total_violations">
                      Total violations: {this.state.total_vioaltions}
                    </h6>
                    <div className="violation_cases_details_filter">
                      <h6>Filter by: </h6>
                      <input className="filter_datee" type="date" id="date" name="date" />
                      
                      <h4 className="bar">|</h4>
                      <button type="button" class="now">
                        Now
                      </button>
                    </div>
                    <Table className="violation_table" />

                    <Card.Text className="violation_content_card_body_text_subheadings_lasttwo">
                      Action
                    </Card.Text>
                    <Divider className="violation_divider" />
                    <div className="violation_action_buttons">
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
                    <Divider className="violation_divider" />
                  </Collapsible>
                </div>
              </Card.Body>
            </Card>
          </div>
        </div>
      </div>
    );
  }
}
export default Violation;
