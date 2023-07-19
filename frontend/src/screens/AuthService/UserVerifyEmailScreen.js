import "../../css/AuthService/VerifyEmail/UserVerifyEmailScreen.css";

import { Col, Image, Row } from "react-bootstrap";
import { EMAIL_VERIFICATION_FAILURE_IMAGE, EMAIL_VERIFICATION_SUCCESS_IMAGE } from "../../constants/imageConstants";
import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import AlertMessage from "../../components/AlertMessages/AlertMessage";
import { useParams } from "react-router-dom";
import { verifyUserEmail } from "../../actions/authActions";

function UserVerifyEmailScreen() {
    const { id, token } = useParams();
    const dispatch = useDispatch();
    const [verifiedStatus, setVerifiedStatus] = useState(false)

    const userRegisterDetails = useSelector(state => state.userRegisterDetails)
    const { error, isLoading, isUserRegistered, isUserVerified } = userRegisterDetails

    if(!verifiedStatus && !isLoading && !isUserVerified && id && token) {
        dispatch(verifyUserEmail(id, token))
        setVerifiedStatus(true)
    }

    return (
        <Row className="verify-email-container">
            <Col md={7}>
                {   !isLoading && isUserRegistered && isUserVerified &&
                    <>
                        <AlertMessage variant="success">
                            The email verification process has been completed successfully.
                            You may now close this tab.
                        </AlertMessage>
                        <Image src={EMAIL_VERIFICATION_SUCCESS_IMAGE} alt="email-verification" fluid />
                    </>
                }
                {
                    error &&
                    <>
                        <AlertMessage variant="danger">
                            The email verification has failed due to either an invalid token or non-existent user.
                            Try again after a while.
                        </AlertMessage>
                        <Image src={EMAIL_VERIFICATION_FAILURE_IMAGE} alt="email-verification" fluid />
                    </>
                }
            </Col>
        </Row>
    )
}

export default UserVerifyEmailScreen