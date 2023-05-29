import React from "react";
import { BsStarFill, BsStarHalf, BsStar } from 'react-icons/bs';
import { Row, Col, OverlayTrigger, Tooltip } from 'react-bootstrap';
import '../../../css/ProductSearchScreen/ProductCard/Rating.css';

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
            <div className="rating-review-container">
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

                <div className="review-count">
                    {
                        text && <span data-testid="review-count">{ text }</span>
                    }
                </div>
            </div>
        </Row>
    );
}

export default Rating;