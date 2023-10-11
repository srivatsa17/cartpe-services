import '../../css/Header/Navbar.css';

import { CART_SCREEN, HOME_SCREEN, WISHLIST_SCREEN } from '../../constants/routes';
import { Container, Nav, NavDropdown, Navbar } from 'react-bootstrap';
import { FaRegHeart, FaRegUser, FaShoppingCart } from 'react-icons/fa';
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import CategoryDropdown from './CategoryDropdown';
import { LOGIN_USER_SCREEN } from '../../constants/routes';
import { LinkContainer } from 'react-router-bootstrap';
import SearchBar from './SearchBar';
import { logoutUser } from '../../actions/authActions';
import { useNavigate } from 'react-router-dom';

function Header() {
    const brandLogo = "/images/cartpe-logo.png";
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const cart = useSelector(state => state.cart);
    const { cartItems } = cart;

    const loginDetails = useSelector(state => state.userLoginDetails)
    const { isLoggedOut } = loginDetails

    const handleUserLogout = () => {
        dispatch(logoutUser())
    }

    useEffect(() => {
        if(isLoggedOut === true) {
            navigate(LOGIN_USER_SCREEN)
        }
    }, [isLoggedOut, navigate])

    return (
        <header>
            <Navbar collapseOnSelect expand="xl" bg="dark" variant="dark" className='p-3' data-testid="navbar">
                <Container>
                    <LinkContainer to={HOME_SCREEN}>
                        <Navbar.Brand>
                            <img src={brandLogo} alt="brandLogo" className="brandLogo" />
                        </Navbar.Brand>
                    </LinkContainer>

                    <Navbar.Toggle aria-controls="basic-navbar-nav" />

                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className='me-auto'>
                            <CategoryDropdown  />
                        </Nav>

                        <Nav>
                            <SearchBar />
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
                                // show={show}
                                // onMouseEnter={showProfileDropdown}
                                // onMouseLeave={hideProfileDropdown}
                            >
                                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.2">
                                    Another action
                                </NavDropdown.Item>
                                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                <NavDropdown.Divider />

                                <div onClick={handleUserLogout} className="nav-buttons">
                                    Logout
                                </div>
                            </NavDropdown>

                            <Nav.Item>
                                <LinkContainer to={WISHLIST_SCREEN}>
                                    <Nav.Link>
                                        <span>
                                            <FaRegHeart className='icons'/> Wishlist
                                        </span>
                                    </Nav.Link>
                                </LinkContainer>
                            </Nav.Item>

                            <Nav.Item>
                                <LinkContainer to={CART_SCREEN}>
                                    <Nav.Link>
                                        {
                                            <div className="cart-icon-container">
                                                <FaShoppingCart className='cart-icon'/>
                                                { cartItems.length > 0 && <span className="cart-quantity">{cartItems.length}</span> }
                                                <span>Cart</span>
                                            </div>
                                        }
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