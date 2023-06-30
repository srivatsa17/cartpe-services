import { Spinner } from "react-bootstrap";

function Loader({ as, animation, size, role, variant }) {
    return (
        <Spinner
            as={as}
            animation={animation}
            role={role}
            size={size}
            variant={variant}
        />
    )
}

export default Loader