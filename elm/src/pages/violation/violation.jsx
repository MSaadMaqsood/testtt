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
import NewTable from "./NewTable";
import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";
import { Link, useParams } from "react-router-dom";

class Violation extends Component {
  constructor(props) {
    super(props);
    
    var url = window.location.href;
    var id = url.substring(url.lastIndexOf("/") + 1);
    this.state = {
      total_vioaltions: 0,
      street_id: id,
      street_name: "",
      street_health: {
        "street_risk_rate": 0,
        "green_index": 0,
        "Asphalt": 100,
        "Sidewalk": 100,
        "Lighting": 100,
        "Cleanliness": 100,
        "Afforestation": 100,
        "Fossils": 100,
        "Rubble_source": 100,
        "Street_Sweeping": 100,
        "Median": 100,
        "Communication_tower": 100,
        "Fly_Poster":100,
        
        "Total_Min_Asphalt": 0,
        "Total_Maj_Asphalt": 0,
        "Total_Sidewalk":0,
        "Total_Lighting": 0,
        "Total_Cleanliness": 0,
        "Total_Afforestation": 0,
        "Total_Fossils": 0,
        "Total_Rubble_source": 0,
        "Total_Street_Sweeping": 0,
        "Total_Median": 0,
        "Total_Communication_tower": 0,
        "Total_Fly_Poster":0
    },
      list_of_streets: [],
      violation_table: {"myData": [], "pages": 1,"tree_Count":0 },
      to_show_violation_table:{"myData": [], "pages": 1, "tree_Count":0},
      render: false,
      selected_date: "",
      to_render:false,
      
      };

    this.GetData = this.GetData.bind(this);
    this.date_change_now = this.date_change_now.bind(this);
    this.date_change = this.date_change.bind(this);
    this.export_pdf = this.export_pdf.bind(this);
    this.GetData();
    console.log(sessionStorage.getItem("username"));
  }

  GetData() {
    const com = this;
    const axios = require("axios").default;
    axios
      .get(
        this.props.server+"/get_violation_page/" + this.state.street_id
      )
      .then(function (response) {
        com.setState({
          street_name: response.data.street_name,
          street_health: response.data.street_health,
          violation_table: response.data.violation_table,
          to_show_violation_table: response.data.violation_table,
          list_of_streets: response.data.list_of_streets,
          total_vioaltions: response.data.violation_table.myData.length,
          render: true
        });
      });
  }

  change = (e) => {
    window.location.href = "/violation/" + e.target.value;
  };
  date_change = (e) => {
    
    const da = e.target.value.split("-");
    const got_date= da[0]+','+da[1]+','+da[2];
    this.setState({
      selected_date: e.target.value
    })
    const com = this;
    const axios = require("axios").default;
    axios
      .get(
        this.props.server+"/get_violation_table_by_date/" + this.state.street_id+"/"+got_date
      )
      .then(function (response) {
        com.setState({
          to_show_violation_table: response.data,
          total_vioaltions: response.data.myData.length,
        });
        
      });
  };
  date_change_now () {
    const temp = this.state.violation_table
    this.setState({
      to_show_violation_table: temp,
      total_vioaltions: temp.myData.length,
      selected_date:""
    })
  };

  export_pdf(){
    var se_date;
    if(this.state.selected_date === ""){
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, '0');
      var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
      var yyyy = today.getFullYear();

      se_date = yyyy+'-'+mm + '-' + dd;
    }else{
      se_date = this.state.selected_date;
    }
  const server = this.props.server;
   const axios = require('axios').default;
    axios.post(this.props.server+"/export_violation_pdf", {'street_name': this.state.street_name, 'street_info': this.state.street_health, 'violation_date':se_date, 'violation_table_data':this.state.to_show_violation_table})
    .then(function (response) {
      
        window.open(server+"/getpdf/"+response.data.pdf_name);
    })

  }
  render() {
      
    const get_streets = this.state.list_of_streets.map((O) => {
      return <option value={O.street_id}>{O.street_name}</option>;
    });
    var table_send = () =>{
      if(this.state.to_render){
        
      }
    }
   

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
                  {this.state.street_health.street_risk_rate}
                  %
                </Card.Title>
                <Card.Text className="violation_content_card_body_text">
                  These cases related to{" "}
                  {this.state.street_name}{" "}
                  street
                </Card.Text>
                <Box
                  sx={{
                    width: this.state.render
                      ? (this.state.street_health.green_index / 3).toString() +
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
                  <option>{this.state.street_name}</option>
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
                          ? this.state.street_health.Asphalt.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Asphalt > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Asphalt >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Asphalt}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Fly Poster Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.state.street_health.Fly_Poster.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Fly_Poster > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Fly_Poster >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Fly_Poster}
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
                          ? this.state.street_health.Lighting.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Lighting > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Lighting >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Lighting}
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
                          ? this.state.street_health.Cleanliness.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Cleanliness > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Cleanliness >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Cleanliness}
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
                          ? this.state.street_health.Afforestation.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Afforestation > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Afforestation >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Afforestation}
                        %
                      </p>
                    </Box>
                  </Card>
                  </div>  
                  <div className="violation_content_cards_02">
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Fossils Health
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.state.street_health.Fossils.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Fossils > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Fossils >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Fossils}
                        %
                      </p>
                    </Box>
                  </Card>

                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Rubble Source
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.state.street_health.Rubble_source.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Rubble_source > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Rubble_source >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Rubble_source}
                        %
                      </p>
                    </Box>
                  </Card>

                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Street Sweeping
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.state.street_health.Street_Sweeping.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Street_Sweeping > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Street_Sweeping >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Street_Sweeping}
                        %
                      </p>
                    </Box>
                  </Card>

                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Median
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? this.state.street_health.Median.toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Median > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Median >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Median}
                        %
                      </p>
                    </Box>
                  </Card>
                  <Card className="violation_content_card">
                    <Card.Title className="violation_status_card_title">
                      Communication Tower
                    </Card.Title>
                    <Box
                      sx={{
                        width: this.state.render
                          ? (this.state.street_health.Communication_tower).toString() +
                            "%"
                          : "0",
                        height: 25,
                        backgroundColor:
                          this.state.render &&
                          this.state.street_health.Communication_tower > 70
                            ? "#00c04b"
                            : this.state.render &&
                              this.state.street_health.Communication_tower >= 50
                            ? "orange"
                            : "red",
                        marginTop: "15px",
                        marginLeft: "0px",
                      }}
                    >
                      <p className="violation_status_card_box_text">
                        {this.state.render &&
                          this.state.street_health.Communication_tower}
                        %
                      </p>
                    </Box>
                  </Card>
                  </div>
                <div>
                  <Box
                    sx={{
                      width: this.state.render
                        ? this.state.street_health.green_index.toString() + "%"
                        : "0",
                      height: 25,
                      backgroundColor: "#00c04b",
                      marginTop: "15px",
                      float: "left",
                    }}
                  >
                    <p className="GreenIndex">
                      Green Index:{" "}
                      {this.state.render && this.state.street_health.green_index}%
                    </p>
                  </Box>
                  <Box
                    sx={{
                      width: this.state.render
                        ? (
                            100 - this.state.street_health.green_index
                          ).toString() + "%"
                        : "0",
                      height: 25,
                      backgroundColor:
                        this.state.render &&
                        this.state.street_health.green_index >= 50
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
                  <div  class="violation_cases_details_tree_count">
                        <h4>Trees Count: {this.state.to_show_violation_table.tree_Count}</h4>
                  </div>
                  <Collapsible trigger={<ExpandCircleDownIcon />}>
                    <Divider className="violation_divider" />
                    
                    <h6 className="violation_cases_deatils_total_violations">
                      Total violations: {this.state.total_vioaltions}
                    </h6>
                    
                    <div className="violation_cases_details_filter">
                      <h6>Filter by: </h6>
                      <input className="filter_datee" type="date" id="date" name="date" onChange={this.date_change} value={this.state.selected_date}/>
                      
                      <h4 className="bar">|</h4>
                      <button type="button" class="now" onClick={this.date_change_now}>
                        Now
                      </button>
                      <button type="button" class="violation_cases_details_filter_export" onClick={this.export_pdf}>
                        Export as PDF
                      </button>
                    </div>
                    <NewTable table_data = {this.state.to_show_violation_table} ref={this.child} changed="true" server={this.props.server}/>

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
