import React, { useState } from 'react';
import { Navbar, Container, Nav, NavDropdown, FormControl, Form, Button } from 'react-bootstrap';
import { FaShoppingCart, FaRegHeart, FaRegUser } from 'react-icons/fa';
import '../css/Header.css';
import { LinkContainer } from 'react-router-bootstrap';

function Header() {
    const brandLogo = "/images/cartpe-logo.png";

    const [show, setShow] = useState(false);
    const showProfileDropdown = () => {
        setShow(!show);
    }

    const hideProfileDropdown = () => {
        setShow(false);
    }

    return (
        <header>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark" className='p-3' data-testid="navbar">
                <Container>
                    <LinkContainer to="/">
                        <Navbar.Brand>
                            <img src={brandLogo} alt="brandLogo" className="brandLogo" />
                        </Navbar.Brand>
                    </LinkContainer>

                    <Navbar.Toggle aria-controls="basic-navbar-nav" />

                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className='me-auto'>
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
                        </Nav>

                        <Nav className='me-auto'>
                            <Form className="d-flex py-2">
                                <FormControl
                                    type="search"
                                    placeholder="Search"
                                    className="me-2 searchBar"
                                    aria-label="Search"
                                    data-testid="Searchbar"
                                />
                                <Button variant="outline-success">Search</Button>
                            </Form>
                        </Nav>

                        <Nav className="justify-content-end">
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
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </header>
    );
}

export default Header;