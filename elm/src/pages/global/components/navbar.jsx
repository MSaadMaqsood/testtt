import { React, Component } from 'react';
import "../style/style.css";
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import { Search, PencilFill, BellFill, PersonFill} from 'react-bootstrap-icons';

class TopNavbar extends Component{
    constructor(props){
        super(props);
        this.state = {

        };
    }

    render() {
        return (
            <div>
                <Navbar className='dashboard_navbar' bg="dark" variant="dark"   fixed="top">
                    
                        <Navbar.Brand className='dashboard_navbar_logo'>
                           <Form.Label htmlFor="inputPassword5">Eye</Form.Label>
                        </Navbar.Brand>
                        <Nav className="m-auto">
                            
                        </Nav>
                        <Nav  className="justify-content-end">
                            <PencilFill color="white" className="dashboard_navbar_icon" size={24}/>
                            <BellFill color="white" className="dashboard_navbar_icon" size={24}/>
                            <PersonFill color="white" className="dashboard_navbar_icon" size={24}/>
                        </Nav>
                    
                </Navbar>
                
                 
          </div>  
        );
    }
}
export default TopNavbar;