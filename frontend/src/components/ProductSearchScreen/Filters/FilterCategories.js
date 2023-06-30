import CollapsibleList from "./CollapsibleList";
import FilterButtonToggle from "./FilterButtonToggle";
import React from "react";
import { useSearchParams } from "react-router-dom";

function FilterCategories({ uniqueCategories, selectedCategories, setSelectedCategories, handleCategories }) {
    const [queryParams, setQueryParams] = useSearchParams();
    const filteredCategories = queryParams.get('categories')?.split(',') ?? [];
    const isCategoryFiltersApplied = filteredCategories.length > 0;

    return (
        <CollapsibleList
            defaultVisible={isCategoryFiltersApplied}
            title="CATEGORIES"
            tooltipTitle="Categories"
            actionButton={
                <FilterButtonToggle
                    visible={selectedCategories.length > 0}
                    active={isCategoryFiltersApplied}
                    onApply={() => {
                        queryParams.set('categories', selectedCategories.join(','));
                        setQueryParams(queryParams, { replace : true });
                    }}
                    onClear={() => {
                        queryParams.delete('categories');
                        setSelectedCategories([]);
                        setQueryParams(queryParams);
                    }}
                />
            }
        >
        {
            uniqueCategories?.filter((category) => {
                return isCategoryFiltersApplied ? filteredCategories.includes(category) : true;
            }).map((category, index) => {
                return (
                    <div key={index} className="filter-type">
                        <input
                            type="checkbox"
                            disabled={filteredCategories.includes(category)}
                            checked={selectedCategories.includes(category)}
                            onChange={() => handleCategories(category)}
                        />
                        <div className="filter-item">{category}</div>
                    </div>
                )
            })
        }
        </CollapsibleList>
    )
}

export default FilterCategories