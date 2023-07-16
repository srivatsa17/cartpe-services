import CollapsibleList from "./CollapsibleList";
import FilterButtonToggle from "./FilterButtonToggle";
import { Form } from "react-bootstrap"
import React from "react";
import { useSearchParams } from "react-router-dom";

function FilterBrands({ uniqueBrands, selectedBrands, setSelectedBrands, handleBrands }) {
    const [queryParams, setQueryParams] = useSearchParams();
    const filteredBrands = queryParams.get('brands')?.split(',') ?? [];
    const isBrandFiltersApplied = filteredBrands.length > 0;

    return (
        <CollapsibleList
            defaultVisible={isBrandFiltersApplied}
            title="BRANDS"
            tooltipTitle="Brands"
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
                        <Form.Check
                            label={brand}
                            disabled={filteredBrands.includes(brand)}
                            checked={selectedBrands.includes(brand)}
                            onChange={() => handleBrands(brand)}
                        />
                    </div>
                )
            })
        }
        </CollapsibleList>
    )
}

export default FilterBrands