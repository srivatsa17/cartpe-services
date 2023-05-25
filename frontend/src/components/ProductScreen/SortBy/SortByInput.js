import React from 'react';
import { SlArrowDown } from 'react-icons/sl';
import { useSearchParams, useLocation } from 'react-router-dom';
import '../../../css/ProductSearchScreen/SortBy/SortByInput.css';

function SortByInput({ handleSortByMenuOnMouseOver, selectedSortByValue, sortByOptions }) {
    const location = useLocation();
    const [queryParams] = useSearchParams();
    const sortByValue = queryParams.get('sort') ?? "";
    const foundOption = sortByOptions.find((option) => option.value === sortByValue);

    const sortByTextPlaceholder = "Sort By: ";
    const defaultSortByValue = "Recommended";

    const getSortByLabel = () => {
        // Reset SortBy option on navigating to another ProductSearchScreen
        if (location.state && location.state.resetSortTitle) {
            return defaultSortByValue
        }

        if(selectedSortByValue) {
            return selectedSortByValue;
        } else {
            if(foundOption) {
                return foundOption.label;
            } else {
                return defaultSortByValue;
            }
        }
    }

    return (
        <div className="sort-by-input" onMouseOver={() => handleSortByMenuOnMouseOver(true)}>
            <div className="sort-by-selected-value">
                {sortByTextPlaceholder}
                <strong>
                    { getSortByLabel() }
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