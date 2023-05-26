import React from "react";
import { useSearchParams } from "react-router-dom";
import CollapsibleList from "./CollapsibleList";
import FilterButtonToggle from "./FilterButtonToggle";

function FilterColors({ uniqueColors, selectedColors, setSelectedColors, handleColors }) {
    const [queryParams, setQueryParams] = useSearchParams();
    const filteredColors = queryParams.get('colors')?.split(',') ?? [];
    const isColorsFiltersApplied = filteredColors.length > 0;

    return (
        <CollapsibleList
            defaultVisible={isColorsFiltersApplied}
            title="COLORS"
            actionButton={
                <FilterButtonToggle
                    visible={selectedColors.length > 0}
                    active={isColorsFiltersApplied}
                    onApply={() => {
                        queryParams.set('colors', selectedColors.join(','));
                        setQueryParams(queryParams, { replace : true });
                    }}
                    onClear={() => {
                        queryParams.delete('colors');
                        setSelectedColors([]);
                        setQueryParams(queryParams);
                    }}
                />
            }
        >
        {
            uniqueColors?.filter((color) => {
                return isColorsFiltersApplied ? filteredColors.includes(color) : true;
            }).map((color, index) => {
                return (
                    <div key={index} className="filter-type">
                        <input
                            type="checkbox"
                            disabled={filteredColors.includes(color)}
                            checked={selectedColors.includes(color)}
                            onChange={() => handleColors(color)}
                        />
                        <div className="color-circle" style={{ backgroundColor: `${color}` }}></div>
                        <div className="filter-item">{color}</div>
                    </div>
                )
            })
        }
        </CollapsibleList>
    )
}

export default FilterColors