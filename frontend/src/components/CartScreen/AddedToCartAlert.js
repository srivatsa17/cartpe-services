import { Alert } from "react-bootstrap";
import React from "react";

function AddedToCartAlert({ closeAlertHandler, alertMessage, alertVariant }) {
    return (
        <Alert variant={alertVariant} onClick={() => closeAlertHandler()} dismissible>
            <Alert.Heading>{alertMessage}</Alert.Heading>
        </Alert>
    )
}

export default AddedToCartAlert