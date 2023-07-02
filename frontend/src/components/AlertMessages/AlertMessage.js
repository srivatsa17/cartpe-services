import { Alert } from "react-bootstrap";
import { useState } from "react";

function AlertMessage({ variant, children }) {
    const [, setShow] = useState(true);

    return (
        <Alert variant={variant} onClose={() => setShow(false)} dismissible>
            {children}
        </Alert>
    );
}

export default AlertMessage