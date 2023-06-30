import "../../css/AuthService/Login/UserLoginScreen.css";

import { Button, Col, Form, Image, InputGroup, OverlayTrigger, Row, Tooltip } from 'react-bootstrap';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { HOME_SCREEN, REGISTER_USER_SCREEN, RESET_PASSWORD_SCREEN } from "../../constants/routes";
import { Link, useNavigate } from 'react-router-dom';
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import ErrorMessage from "../../components/ErrorMessages/ErrorMessage";
import Loader from "../../components/Loader/Loader";
import { loginUser } from '../../actions/authActions';

function UserLoginScreen() {
    const loginUserImage = "/images/login.png";
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        isEmailValid: false,
        isPasswordValid: false,
        invalidEmailMessage: '',
        showPassword: false
    })

    const { email, password, isEmailValid, isPasswordValid, invalidEmailMessage, showPassword} = formData;

    const handleEmailChange = (e) => {
        const newEmail = e.target.value;
        setFormData((previousFormData) => ({
            ...previousFormData,
            email: newEmail,
            isEmailValid: newEmail.match(/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i) !== null,
            invalidEmailMessage: newEmail ? "Please enter a valid email address." : ""
        }))
    };

    const handlePasswordChange = (e) => {
        const newPassword = e.target.value;
        setFormData((previousFormData) => ({
            ...previousFormData,
            password: newPassword,
            isPasswordValid: newPassword.length >= 8 && /[a-zA-Z]/.test(newPassword) && /\d/.test(newPassword)
        }))
    };

    const handleToggleShowPassword = () => {
        setFormData((previousFormData) => ({
            ...previousFormData,
            showPassword: !previousFormData.showPassword
        }))
    };

    const invalidPasswordMessage = (password) => {
        if(password.length < 8) return "Password should be at least 8 characters long.";
        else if (!/[a-zA-Z]/i.test(password)) return "Password should contain alphabets.";
        else if (!/\d/.test(password)) return "Password should contain digits.";
        return "";
    }

    const userDetails = useSelector(state => state.userDetails)
    const { error, loading, isLoggedIn } = userDetails

    useEffect(() => {
        if(isLoggedIn === true) {
            navigate(HOME_SCREEN);
        }
    }, [isLoggedIn, navigate])

    const handleLoginClick = (event) => {
        event.preventDefault();
        dispatch(loginUser(email, password));
    }

    return (
        <Row className="login-user-container">
            <Col xs={6} sm={6} md={6} lg={6} xl={6}>
                <Image className="login-user-image" src={loginUserImage} alt="login" />
            </Col>
            <Col lg={5} xl={4}>
                { error && <ErrorMessage>{error}</ErrorMessage> }
                <div className="login-heading">
                    Login to <span id="brand-name">CartPe</span>!
                </div>
                <Form.Group>
                    <Form.Label htmlFor="email" className="email-label">Email</Form.Label>
                    <Form.Control
                        type="email"
                        className={email.length > 0 && (isEmailValid ? 'is-valid' : 'is-invalid')}
                        placeholder="john.doe@example.com"
                        value={email}
                        onChange={handleEmailChange}
                        required
                    />
                    {   isEmailValid ? (
                            <Form.Control.Feedback className="valid-feedback py-1">
                                Email looks good!
                            </Form.Control.Feedback>
                        ) : (
                            <Form.Control.Feedback className="invalid-feedback py-1">
                                {invalidEmailMessage}
                            </Form.Control.Feedback>
                        )
                    }
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="password" className="password-label">Password</Form.Label>
                    <InputGroup hasValidation>
                        <Form.Control
                            type={showPassword ? 'text' : 'password'}
                            className={password.length > 0 && (isPasswordValid ? 'is-valid' : 'is-invalid')}
                            value={password}
                            onChange={handlePasswordChange}
                            required
                        />
                        <InputGroup.Text
                            className="show-password-icon"
                            onClick={handleToggleShowPassword}
                        >
                            <OverlayTrigger
                                placement="top"
                                overlay={
                                    <Tooltip>
                                        {showPassword ? "Hide password" : "Show password"}
                                    </Tooltip>
                                }
                            >
                                <div className="show-password-icon">
                                    { showPassword ? <FaEye /> : <FaEyeSlash /> }
                                </div>
                            </OverlayTrigger>
                        </InputGroup.Text>
                        {
                            isPasswordValid ? (
                                <Form.Control.Feedback className="valid-feedback py-1">
                                    Password looks good!
                                </Form.Control.Feedback>
                            ) : (
                                <Form.Control.Feedback className="invalid-feedback py-1">
                                    {invalidPasswordMessage(password)}
                                </Form.Control.Feedback>
                            )
                        }
                    </InputGroup>
                </Form.Group>
                {
                    loading ?
                    <Button
                        variant="dark"
                        className="login-button"
                        disabled
                    >
                        <Loader
                            as="span"
                            animation="border"
                            size="sm"
                            role="status"
                            aria-hidden="true"
                        />
                        <span className="mx-2">Loading...</span>
                    </Button>
                    :
                    <Button
                        variant="dark"
                        className="login-button"
                        disabled={!(isEmailValid && isPasswordValid)}
                        onClick={handleLoginClick}
                    >
                        Login
                    </Button>
                }
                <div className="reset-password-link-container">
                    Can't remember password?
                    <Link to={RESET_PASSWORD_SCREEN} className="reset-password-link-button">
                        Reset password
                    </Link>
                </div>
                <div className="register-link-container">
                    Don't have an account?
                    <Link to={REGISTER_USER_SCREEN} className="register-link-button">
                        Register
                    </Link>
                </div>
            </Col>
        </Row>
    );
}

export default UserLoginScreen;