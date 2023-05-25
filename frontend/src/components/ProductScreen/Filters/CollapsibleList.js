import React, { useState } from "react";
import { Row } from 'react-bootstrap';
import '../../../css/ProductSearchScreen/Filters/CollapsibleList.css';

function CollapsibleList({ title, children, actionButton, defaultVisible}) {
    const [visible, setVisible] = useState(defaultVisible);

    return (
        <Row>
            <div className="collapsible-container">
                <button className="collapsible-button" onClick={() => setVisible((visible) => !visible)}>
                    <div>{title}</div>
                </button>
                <div>{actionButton}</div>
            </div>
            {visible ? <div>{children}</div> : null}
        </Row>
    );
}

export default CollapsibleList;