import React, { useState } from "react";
import { Row } from 'react-bootstrap';
import { useSearchParams } from "react-router-dom";

function FilterDiscounts({ discount, handleDiscounts }) {
    const discountsList = Array.from({ length: 9 }, (_, index) => (index + 1) * 10);
    const [isChecked, setIsChecked] = useState(false)
    const [queryParams] = useSearchParams();
    const discountFromQueryParams = Number(queryParams.get('discount'))

    const handleChange = (discountValue) => {
        if((isChecked && discountValue === discount) || (discountValue === discountFromQueryParams)) {
            setIsChecked(false)
            handleDiscounts(null)
        } else {
            setIsChecked(true)
            handleDiscounts(discountValue)
        }
    }

    return (
        <Row>
            <h6>DISCOUNT RANGE</h6>
            {
                discountsList.map((discountOption, index) => {
                    return (
                        <div key={index} className="filter-type">
                            <input
                                type="checkbox"
                                checked={discountOption === discountFromQueryParams || discountOption === discount}
                                onChange={() => handleChange(discountOption)}
                            />
                            <div className="filter-item">{discountOption}% and above</div>
                        </div>
                    )
                })
            }
        </Row>
    );
}

export default FilterDiscounts;