import React, { useState } from 'react';
import { Navbar, Container, Nav, NavDropdown, Form, Button } from 'react-bootstrap';
import { FaShoppingCart, FaRegHeart, FaRegUser } from 'react-icons/fa';
import '../css/Header.css';

function Header() {
    const brandLogo = "/images/favicon.ico";
    
    const [show, setShow] = useState(false);
    const showProfileDropdown = (e) =>{
        setShow(!show);
    }

    const hideProfileDropdown = (e) => {
        setShow(false);
    }

    return (
        <header>
            <Navbar collapseOnSelect expand="md" bg="dark" variant="dark" className='p-3'>
                <Container>
                    <Nav>
                        <Navbar.Brand href="#home">
                            <img src={brandLogo} alt="logo" className="brandLogo" /> CartPe
                        </Navbar.Brand>

                        <Nav.Item>
                            <NavDropdown 
                                title="Categories" 
                                id="collapsible-nav-dropdown"
                            >
                                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.2">
                                    Another action
                                </NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="#action/3.4">
                                    Separated link
                                </NavDropdown.Item>
                            </NavDropdown>
                        </Nav.Item>

                        <Nav.Item>
                            <Form className="d-flex searchForm">
                                <Form.Control
                                    type="search"
                                    placeholder="Search"
                                    className="me-3 searchBar"
                                    aria-label="Search"
                                />
                                <Button variant="outline-success">Search</Button>
                            </Form>
                        </Nav.Item>
                    </Nav>
                    
                    <Nav>
                        <Nav.Item>
                            <NavDropdown 
                                title={
                                    <span>
                                        <FaRegUser className='icons'/> Profile
                                    </span>
                                }
                                id="collapsible-nav-dropdown"
                                show={show}
                                onMouseEnter={showProfileDropdown} 
                                onMouseLeave={hideProfileDropdown}
                            >
                                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.2">
                                    Another action
                                </NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="#action/3.4">
                                    Separated link
                                </NavDropdown.Item>
                            </NavDropdown>
                        </Nav.Item>

                        <Nav.Item>
                            <Nav.Link href="#wishlist">
                                <span>
                                    <FaRegHeart className='icons'/> Wishlist
                                </span>
                            </Nav.Link>
                        </Nav.Item>

                        <Nav.Item>
                            <Nav.Link href="#cart">
                                <span>
                                    <FaShoppingCart className='icons'/> Cart
                                </span>
                            </Nav.Link>
                        </Nav.Item>
                    </Nav>
                </Container>
            </Navbar>
        </header>
    );
}

export default Header;