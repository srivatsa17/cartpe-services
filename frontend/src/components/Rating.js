import React from "react";
import { BsStarFill, BsStarHalf, BsStar } from 'react-icons/bs';
import { Row, Col, OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../css/Rating.css';

function createStars(ratingObj) {
    var stars = [];
    var ratingIntPart = Math.trunc(ratingObj.rating);
    var ratingDecimalPart = Number((ratingObj.rating - ratingIntPart).toFixed(2));
    var count = 0;

    if(ratingIntPart < 0) {
        ratingIntPart = 0;
        ratingDecimalPart = 0;
    }

    for(let i = 0; i < ratingIntPart && i < 5; i++){
        count++;
        stars.push(
            <span key={count}>
                <BsStarFill data-testid="full-star"/>
            </span>
        );
    }

    if(ratingDecimalPart >= 0.5 && count < 5) {
        count++;
        stars.push(
            <span key={count}>
                <BsStarHalf data-testid="half-star"/>
            </span>
        );
    }

    for(let i = count; i < 5; i++){
        count++;
        stars.push(
            <span key={count}>
                <BsStar data-testid="empty-star"/>
            </span>
        );
    }
    
    return stars; 
}

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
                    <div className="ratings" data-testid="ratings">
                        { createStars({ rating }) }
                    </div>
                </OverlayTrigger>
            </Col>

            <Col>
                {
                    text && <span data-testid="review-count">{ text }</span>
                }
            </Col>
        </Row>
    );
}

export default Rating;