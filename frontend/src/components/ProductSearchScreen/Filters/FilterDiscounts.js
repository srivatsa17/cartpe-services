import React, { useState } from "react";

import CollapsibleList from "./CollapsibleList";
import { useSearchParams } from "react-router-dom";

function FilterDiscounts({ discountRanges, discount, handleDiscounts }) {
    const [isChecked, setIsChecked] = useState(false)
    const [queryParams] = useSearchParams();
    const discountFilterApplied = Number(queryParams.get('discount'))

    const handleChange = (discountValue) => {
        if((isChecked && discountValue === discount) || (discountValue === discountFilterApplied)) {
            setIsChecked(false)
            handleDiscounts(null)
        } else {
            setIsChecked(true)
            handleDiscounts(discountValue)
        }
    }

    return (
        <CollapsibleList
            defaultVisible={discountFilterApplied}
            title="DISCOUNT RANGES"
            tooltipTitle="Discounts"
        >
        {
            discountRanges.map((discountOption, index) => {
                return (
                    <div key={index} className="filter-type">
                        <input
                            type="checkbox"
                            checked={discountOption === discountFilterApplied || discountOption === discount}
                            onChange={() => handleChange(discountOption)}
                        />
                        <div className="filter-item">{discountOption}% and above</div>
                    </div>
                )
            })
        }
        </CollapsibleList>
    );
}

export default FilterDiscounts;