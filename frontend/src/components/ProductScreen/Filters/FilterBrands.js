import React from "react";
import { useSearchParams } from "react-router-dom";
import CollapsibleList from "./CollapsibleList";
import FilterButtonToggle from "./FilterButtonToggle";

function FilterBrands({ uniqueBrands, selectedBrands, setSelectedBrands, handleBrands }) {
    const [queryParams, setQueryParams] = useSearchParams();
    const filteredBrands = queryParams.get('brands')?.split(',') ?? [];
    const isBrandFiltersApplied = filteredBrands.length > 0;

    return (
        <CollapsibleList
            defaultVisible={isBrandFiltersApplied}
            title="BRANDS"
            actionButton={
                <FilterButtonToggle
                    visible={selectedBrands.length > 0}
                    active={isBrandFiltersApplied}
                    onApply={() => {
                        queryParams.set('brands', selectedBrands.join(','));
                        setQueryParams(queryParams, { replace : true });
                    }}
                    onClear={() => {
                        queryParams.delete('brands');
                        setSelectedBrands([]);
                        setQueryParams(queryParams);
                    }}
                />
            }
        >
        {
            uniqueBrands?.filter((brand) => {
                return isBrandFiltersApplied ? filteredBrands.includes(brand) : true;
            }).map((brand, index) => {
                return (
                    <div key={index} className="filter-type">
                        <input
                            type="checkbox"
                            disabled={filteredBrands.includes(brand)}
                            checked={selectedBrands.includes(brand)}
                            onChange={() => handleBrands(brand)}
                        />
                        <div className="filter-item">{brand}</div>
                    </div>
                )
            })
        }
        </CollapsibleList>
    )
}

export default FilterBrands