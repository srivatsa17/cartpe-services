import React from 'react';
import { SlArrowDown } from 'react-icons/sl';
import { useSearchParams } from 'react-router-dom';
import '../../../css/ProductSearchScreen/SortBy/SortByInput.css';

function SortByInput({ handleSortByMenuOnMouseOver, selectedSortByValue, sortByOptions }) {
    const sortByTextPlaceholder = "Sort By: ";
    const defaultSortByValue = "Recommended";
    const [queryParams] = useSearchParams();
    const sortByValue = queryParams.get('sort');
    const foundOption = sortByOptions.find((option) => option.value === sortByValue);

    return (
        <div className="sort-by-input" onMouseOver={() => handleSortByMenuOnMouseOver(true)}>
            <div className="sort-by-selected-value">
                {sortByTextPlaceholder}
                <strong>
                    { selectedSortByValue ? selectedSortByValue : foundOption ? foundOption.label : defaultSortByValue }
                </strong>
            </div>
            <div className="sort-by-tools">
                <div className="sort-by-tool">
                    <SlArrowDown />
                </div>
            </div>
        </div>
    );
}

export default SortByInput;