import { React, Component } from "react";

import "../global/style/style.css";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import {
  Search,
  PencilFill,
  BellFill,
  PersonFill,
} from "react-bootstrap-icons";

class TopNavbar extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <Navbar
          className="dashboard_navbar"
          bg="dark"
          variant="dark"
          fixed="top"
        >
          <Navbar.Brand className="dashboard_navbar_logo">
            <Form.Label htmlFor="inputPassword5">Eye</Form.Label>
          </Navbar.Brand>
          {/* <Nav className="m-auto">
            <InputGroup className="mb-2">
              <Form.Control
                placeholder="Search resourses...."
                aria-label="Username"
                aria-describedby="basic-addon1"
                className="dashboard_navbar_search dashboard_navbar_search_width"
              />
              <InputGroup.Text
                id="basic-addon1"
                className="dashboard_navbar_btn"
              >
                <Search />
              </InputGroup.Text>
            </InputGroup>
          </Nav> */}
        </Navbar>
      </div>
    );
  }
}
export default TopNavbar;
