import CollapsibleList from "./CollapsibleList";
import { FaRupeeSign } from "react-icons/fa";
import React from "react";
import { useSearchParams } from "react-router-dom";

function getRupeeSymbol() {
    return (
        <FaRupeeSign className="rupee-icon"/>
    )
}

function FilterPrices({ minAndMaxPrices, selectedPrice, handlePrices }) {
    const [queryParams] = useSearchParams();
    const filteredMaxPrice = queryParams.get('maxPrice') ?? null;
    const isPriceFilterApplied = filteredMaxPrice !== null;

    return (
        <CollapsibleList
            defaultVisible={isPriceFilterApplied}
            title="PRICE RANGE"
            tooltipTitle="Prices"
        >
            <input 
                type="range" 
                onInput={handlePrices} 
                step={100}
                min={minAndMaxPrices.minPrice}
                max={minAndMaxPrices.maxPrice}
                value={filteredMaxPrice ?? minAndMaxPrices.minPrice}
            />
            { isPriceFilterApplied &&
                <h6>
                    Range: {getRupeeSymbol()}{minAndMaxPrices.minPrice} - {getRupeeSymbol()}{ selectedPrice }
                </h6>
            }
        </CollapsibleList>
    )
}

export default FilterPrices