import { Alert } from "react-bootstrap";
import { useState } from "react";

function ErrorMessage({ variant, children }) {
    const [, setShow] = useState(true);

    return (
        <Alert variant={variant} onClose={() => setShow(false)} dismissible>
            {children}
        </Alert>
    );
}

export default ErrorMessage