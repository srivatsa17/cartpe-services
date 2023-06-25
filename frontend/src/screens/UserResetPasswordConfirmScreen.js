import React, { useState } from "react";
import { Button, Row, Col, Form, InputGroup, Image, OverlayTrigger, Tooltip } from 'react-bootstrap';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import "../css/UserResetPasswordConfirmScreen.css";

function UserResetPasswordConfirmScreen() {
    const resetPasswordConfirmImage = "/images/reset-password-confirm.jpg";
    const [formData, setFormData] = useState({
        newPassword: '',
        newConfirmPassword: '',
        isNewPasswordValid: false,
        isNewConfirmPasswordValid: false,
        showNewPassword: false,
        showNewConfirmPassword: false
    })

    const { newPassword, newConfirmPassword, isNewPasswordValid, isNewConfirmPasswordValid, showNewPassword, showNewConfirmPassword } = formData;

    const handleNewPasswordChange = (e) => {
        const newPassword = e.target.value;
        setFormData((previousFormData) => ({
            ...previousFormData,
            newPassword: newPassword,
            isNewPasswordValid: newPassword.length >= 8 && /[a-zA-Z]/.test(newPassword) && /\d/.test(newPassword)
        }))
    };

    const handleNewConfirmPasswordChange = (e) => {
        const newConfirmPassword = e.target.value;
        setFormData((previousFormData) => ({
            ...previousFormData,
            newConfirmPassword: newConfirmPassword,
            isNewConfirmPasswordValid: newConfirmPassword.length >= 8 &&
                                /[a-zA-Z]/.test(newConfirmPassword) &&
                                /\d/.test(newConfirmPassword) &&
                                newPassword === newConfirmPassword
        }))
    };

    const handleToggleShowNewPassword = () => {
        setFormData((previousFormData) => ({
            ...previousFormData,
            showNewPassword: !previousFormData.showNewPassword
        }))
    };

    const handleToggleShowNewConfirmPassword = () => {
        setFormData((previousFormData) => ({
            ...previousFormData,
            showNewConfirmPassword: !previousFormData.showNewConfirmPassword
        }))
    };

    const invalidPasswordMessage = (password) => {
        if(password.length < 8) return "Password should be at least 8 characters long.";
        else if (!/[a-zA-Z]/i.test(password)) return "Password should contain alphabets.";
        else if (!/\d/.test(password)) return "Password should contain digits.";
        else if (newPassword !== newConfirmPassword) return "Passwords are not matching.";
        return "";
    }

    return (
        <Row className="reset-password-confirm-container">
            <Col xs={6} sm={6} md={6} lg={6} xl={6}>
                <Image className="reset-password-confirm-image"
                    src={resetPasswordConfirmImage}
                    alt="reset-password-confirm"
                />
            </Col>
            <Col lg={5} xl={4}>
                <div className="reset-password-confirm-heading">
                    Enter new password!
                </div>
                <Form.Group>
                    <Form.Label htmlFor="password" className="new-password-label">New Password</Form.Label>
                    <InputGroup hasValidation>
                        <Form.Control
                            type={showNewPassword ? 'text' : 'password'}
                            className={newPassword.length > 0 && (isNewPasswordValid ? 'is-valid' : 'is-invalid')}
                            value={newPassword}
                            onChange={handleNewPasswordChange}
                            required
                        />
                        <InputGroup.Text
                            className="show-new-password-icon"
                            onClick={handleToggleShowNewPassword}
                        >
                            <OverlayTrigger
                                placement="top"
                                overlay={
                                    <Tooltip>
                                        {showNewPassword ? "Hide password" : "Show password"}
                                    </Tooltip>
                                }
                            >
                                <div>
                                    { showNewPassword ? <FaEye /> : <FaEyeSlash /> }
                                </div>
                            </OverlayTrigger>
                        </InputGroup.Text>
                        {
                            isNewPasswordValid ?
                                <Form.Control.Feedback className="valid-feedback py-1">
                                    Password looks good!
                                </Form.Control.Feedback>
                            :
                                <Form.Control.Feedback className="invalid-feedback py-1">
                                    {invalidPasswordMessage(newPassword)}
                                </Form.Control.Feedback>
                        }
                    </InputGroup>
                </Form.Group>
                <Form.Group>
                    <Form.Label htmlFor="password" className="new-confirm-password-label">
                        Confirm New Password
                    </Form.Label>
                    <InputGroup hasValidation>
                        <Form.Control
                            type={showNewConfirmPassword ? 'text' : 'password'}
                            className={newConfirmPassword.length > 0 && (isNewConfirmPasswordValid ? 'is-valid' : 'is-invalid')}
                            value={newConfirmPassword}
                            onChange={handleNewConfirmPasswordChange}
                            required
                        />
                        <InputGroup.Text
                            className="show-new-confirm-password-icon"
                            onClick={handleToggleShowNewConfirmPassword}
                        >
                            <OverlayTrigger
                                placement="top"
                                overlay={
                                    <Tooltip>
                                        {showNewConfirmPassword ? "Hide password" : "Show password"}
                                    </Tooltip>
                                }
                            >
                                <div>
                                    { showNewConfirmPassword ? <FaEye /> : <FaEyeSlash /> }
                                </div>
                            </OverlayTrigger>
                        </InputGroup.Text>
                        {
                            isNewConfirmPasswordValid ?
                                <Form.Control.Feedback className="valid-feedback py-1">
                                    Password looks good!
                                </Form.Control.Feedback>
                            :
                                <Form.Control.Feedback className="invalid-feedback py-1">
                                    {invalidPasswordMessage(newConfirmPassword)}
                                </Form.Control.Feedback>
                        }
                    </InputGroup>
                </Form.Group>
                <Button
                    variant="dark"
                    className="reset-password-confirm-button"
                    disabled={!(isNewPasswordValid && isNewConfirmPasswordValid)}
                >
                    Reset Password
                </Button>
            </Col>
        </Row>
    );
}

export default UserResetPasswordConfirmScreen;