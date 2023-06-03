import React from "react";
import { Alert } from "react-bootstrap";

function AddedToCartAlert({ closeAlertHandler, alertMessage, alertVariant }) {
    return (
        <Alert variant={alertVariant} onClick={() => closeAlertHandler()} dismissible>
            <Alert.Heading>{alertMessage}</Alert.Heading>
        </Alert>
    )
}

export default AddedToCartAlert