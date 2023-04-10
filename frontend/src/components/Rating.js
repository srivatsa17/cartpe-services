import React from "react";
import { BsStarFill, BsStarHalf, BsStar } from 'react-icons/bs';
import { Row, Col, OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../css/Rating.css';

function Rating({ rating, text }) {
    return (
        <Row>
            <Col>
                <OverlayTrigger
                    key="bottom"
                    placement="bottom"
                    overlay={
                        <Tooltip id="tooltip-bottom">
                            <strong>{rating} out of 5 stars</strong>
                        </Tooltip>
                    }
                >
                    <div className="ratings">
                        <span>
                            { rating >= 1 ? <BsStarFill id="star"/> : rating >= 0.5 ? <BsStarHalf id="star"/> : <BsStar id="star"/> }
                        </span>
                        <span>
                            { rating >= 2 ? <BsStarFill id="star"/> : rating >= 1.5 ? <BsStarHalf id="star"/> : <BsStar id="star"/> }
                        </span>
                        <span>
                            { rating >= 3 ? <BsStarFill id="star"/> : rating >= 2.5 ? <BsStarHalf id="star"/> : <BsStar id="star"/> }
                        </span>
                        <span>
                            { rating >= 4 ? <BsStarFill id="star"/> : rating >= 3.5 ? <BsStarHalf id="star"/> : <BsStar id="star"/> }
                        </span>
                        <span>
                            { rating >= 5 ? <BsStarFill id="star"/> : rating >= 4.5 ? <BsStarHalf id="star"/> : <BsStar id="star"/> }
                        </span>
                    </div>
                </OverlayTrigger>
            </Col>

            <Col>
                <span>{text && text}</span>
            </Col>
        </Row>
    );
}

export default Rating;