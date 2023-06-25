import React, { useState } from "react";
import { Button, Row, Col, Form, Image } from 'react-bootstrap';
import "../css/UserResetPasswordScreen.css";

function UserResetPasswordScreen() {
    const resetPasswordUserImage = "/images/reset-password.jpg"
    const [formData, setFormData] = useState({
        email: '',
        isEmailValid: false,
        invalidEmailMessage: '',
    })

    const { email, isEmailValid, invalidEmailMessage } = formData;

    const handleEmailChange = (e) => {
        const newEmail = e.target.value;
        setFormData((previousFormData) => ({
            ...previousFormData,
            email: newEmail,
            isEmailValid: newEmail.match(/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i) !== null,
            invalidEmailMessage: newEmail ? "Please enter a valid email address." : ""
        }))
    };

    return (
        <Row className="reset-password-user-container">
            <Col xs={6} sm={6} md={6} lg={6} xl={6}>
                <Image className="reset-password-user-image" src={resetPasswordUserImage} alt="reset-password" />
            </Col>
            <Col lg={5} xl={4}>
                <div className="reset-password-heading">
                    Reset your password!
                </div>
                <Form.Group>
                    <Form.Label className="email-label">Email</Form.Label>
                    <Form.Control
                        type="email"
                        className={email.length > 0 && (isEmailValid ? 'is-valid' : 'is-invalid')}
                        placeholder="john.doe@example.com"
                        value={email}
                        onChange={handleEmailChange}
                        required
                    />
                    {   isEmailValid ?
                            <Form.Control.Feedback className="valid-feedback py-1">
                                Email looks good!
                            </Form.Control.Feedback>
                        :
                            <Form.Control.Feedback className="invalid-feedback py-1">
                                {invalidEmailMessage}
                            </Form.Control.Feedback>
                    }
                </Form.Group>
                <Button
                    variant="dark"
                    className="reset-password-button"
                    disabled={!isEmailValid}
                >
                    Reset Password
                </Button>
            </Col>
        </Row>
    );
}

export default UserResetPasswordScreen;