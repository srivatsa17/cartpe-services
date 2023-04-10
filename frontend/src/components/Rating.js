import React from "react";
import { BsStarFill, BsStarHalf, BsStar } from 'react-icons/bs';
import '../css/Rating.css';

function Rating({ rating, text }) {
    return (
        <div className="ratings" title={`${rating}/5`}>
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
            <span id="text">{text && text}</span>
        </div>
    );
}

export default Rating;