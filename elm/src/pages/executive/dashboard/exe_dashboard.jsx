import { React, Component } from "react";
import "../../global/style/style.css";
import TopNavbar from "../../global/components/navbar";
import Exe_MiniDrawer from "../../global/components/exe_Sidebar";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import { ArrowRight } from "react-bootstrap-icons";
import Exe_MapContainer from "./exe_mymap";
import { Link } from "react-router-dom";
import Box from "@mui/material/Box";

class Exe_Dashboard extends Component {
    constructor(props) {
      super(props);
      this.state = {
        street_health: 0,
        green_index: 0,
        risk: 0,
        data_map: {'line':[],'circle':[]},
        tree_map: {'line':[],'circle':[]},
        render: true,
      };
      this.GetData = this.GetData.bind(this);
   
    this.GetData();
    }
    GetData() {
      const com = this;
      const axios = require("axios").default;
      axios.get(this.props.server+"/get_dashboard").then(function (response) {
        // handle success
  
        com.setState({
          street_health: response.data.street_health,
          green_index: response.data.green_index,
          risk: response.data.risk,
          data_map: response.data.data_map,
          tree_map: response.data.tree_data
        });
      });
    }
    render() {
      return (
        <div>
          <Exe_MiniDrawer />
          <TopNavbar />
          <div className="dashboard_content">
            <div className="dashboard_content_cards">
              <Card className="dashboard_content_card">
                <Card.Body className="dashboard_content_card_body">
                  <Card.Title className="dashboard_content_card_body_title">
                    Street Health
                  </Card.Title>
                  <Card.Text className="dashboard_content_card_body_text">
                    {this.state.street_health}%
                  </Card.Text>
                  <Button variant="outline-primary">
                    Show All Cases <ArrowRight />{" "}
                  </Button>
                </Card.Body>
              </Card>
  
              <Card className="dashboard_content_card">
                <Card.Body className="dashboard_content_card_body">
                  <Card.Title className="dashboard_content_card_body_title">
                    Green Index (Saudi)
                  </Card.Title>
                  <Card.Text className="dashboard_content_card_body_text">
                    {this.state.green_index}%
                  </Card.Text>
                  <Button variant="outline-primary">
                    Show All Cases <ArrowRight />
                  </Button>
                </Card.Body>
              </Card>
              <Card className="dashboard_content_card">
                <Card.Body className="dashboard_content_card_body">
                  <Card.Title className="dashboard_content_card_body_title">
                    Risk
                  </Card.Title>
                  <Card.Text className="dashboard_content_card_body_text_red">
                    {this.state.risk}%
                  </Card.Text>
                  <Link to="/violation/1">
                    <Button variant="outline-primary">
                      Show All Cases <ArrowRight />
                    </Button>
                  </Link>
                </Card.Body>
              </Card>
            </div>
            <div className="dashboard_content_map">
              <h3>Current Street Health</h3>
            <div className="dashboard_street_health_map_color_summary">
              <Box
                sx={{
                  width: 50,
                  height: 15,
                  backgroundColor: "red",
                }}
              />
              <h6 className="key_map">High Risk</h6>
              <h4 className="key_map_bar">|</h4>
              <Box
                sx={{
                  width: 50,
                  height: 15,
                  backgroundColor: "orange",
                }}
              />
              <h6 className="key_map">Normal Risk</h6>
              <h4 className="key_map_bar">|</h4>
              <Box
                sx={{
                  width: 50,
                  height: 15,
                  backgroundColor: "green",
                }}
              />
              <h6 className="key_map">No Risk</h6>
              </div>
              <label>Last update 12h ago</label>
              <div>
                <Exe_MapContainer data={this.state.data_map} tree ={this.state.tree_map}/>
              </div>
            </div>
          </div>
        </div>
      );
    }
}
export default Exe_Dashboard;