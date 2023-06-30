import '../../../css/ProductSearchScreen/Filters/CollapsibleList.css';

import { OverlayTrigger, Row, Tooltip } from 'react-bootstrap';
import React, { useState } from "react";

function CollapsibleList({ title, tooltipTitle, children, actionButton, defaultVisible }) {
    const [visible, setVisible] = useState(defaultVisible);

    return (
        <Row>
            <div className="collapsible-container">
                <button className="collapsible-button" onClick={() => setVisible((visible) => !visible)}>
                    {   !visible ? 
                            <OverlayTrigger placement="top" overlay={ <Tooltip>Click to filter on {tooltipTitle}</Tooltip> }>
                                <div>{title}</div>
                            </OverlayTrigger> 
                        :
                            <div>{title}</div>
                    }
                </button>
                <div>{actionButton}</div>
            </div>
            {visible ? <div>{children}</div> : null}
        </Row>
    );
}

export default CollapsibleList;