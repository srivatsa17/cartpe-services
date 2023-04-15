import React, { useState } from 'react';
import { Navbar, Container, Nav, NavDropdown, Form, Button } from 'react-bootstrap';
import { FaShoppingCart, FaRegHeart, FaRegUser } from 'react-icons/fa';
import '../css/Header.css';
import { LinkContainer } from 'react-router-bootstrap';

function Header() {
    const brandLogo = "/images/cartpe-logo.png";
    
    const [show, setShow] = useState(false);
    const showProfileDropdown = (e) =>{
        setShow(!show);
    }

    const hideProfileDropdown = (e) => {
        setShow(false);
    }

    return (
        <header>
            <Navbar collapseOnSelect expand="md" bg="dark" variant="dark" className='p-3' data-testid="navbar">
                <Container>
                    <Nav>
                        <LinkContainer to="/">
                            <Navbar.Brand>
                                <img src={brandLogo} alt="brandLogo" className="brandLogo" />
                            </Navbar.Brand>
                        </LinkContainer>

                        <Nav.Item>
                            <NavDropdown 
                                title="Categories" 
                                id="collapsible-nav-dropdown"
                                data-testid="categories-dropdown"
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
                                    data-testid="Searchbar"
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
                                data-testid="profile-dropdown"
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
                            <LinkContainer to="/wishlist">
                                <Nav.Link>
                                    <span>
                                        <FaRegHeart className='icons'/> Wishlist
                                    </span>
                                </Nav.Link>
                            </LinkContainer>
                        </Nav.Item>

                        <Nav.Item>
                            <LinkContainer to="/cart">
                                <Nav.Link>
                                    <span>
                                        <FaShoppingCart className='icons'/> Cart
                                    </span>
                                </Nav.Link>
                            </LinkContainer>
                        </Nav.Item>
                    </Nav>
                </Container>
            </Navbar>
        </header>
    );
}

export default Header;