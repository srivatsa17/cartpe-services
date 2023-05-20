import React, { useEffect, useState, useRef } from "react";
import { useSearchParams } from 'react-router-dom';
import { Col } from 'react-bootstrap';
import { SlArrowDown } from 'react-icons/sl';
import '../../css/ProductSearchScreen/SortBy.css';

const sortByOptions = [
    { value : "name", label : "Recommended"},
    { value : "new", label : "What's New"},
    { value : "popularity", label : "Popularity"},
    { value : "discount", label : "Better discount"},
    { value : "price_desc", label : "Price: High to Low"},
    { value : "price_asc", label : "Price: Low to High"},
    { value : "rating", label : "Customer Rating"}
];

function SortBy({ handleSort }) {
    const sortByRef = useRef(null);
    const [showSortByMenu, setShowSortByMenu] = useState(false);
    const [selectedSortByValue, setSelectedSortByValue] = useState(null);
    const [queryParams, setQueryParams] = useSearchParams();
    const sortByTextPlaceholder = "Sort By: ";

    const getSortByDisplay = () => {
        if(selectedSortByValue) {
            return selectedSortByValue.label;
        } else {
            const defaultSortByValue = sortByOptions.find((option) => option.value === queryParams.get('sort'));
            if(defaultSortByValue) {
                return defaultSortByValue.label;
            } else {
                return "";
            }
        } 
    }

    useEffect(() => {
        const handleClickOutside = (event) => {
            if(sortByRef.current && !sortByRef.current.contains(event.target)) {
                setShowSortByMenu(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    })

    const handleSortByMenuOnMouseOver = () => {
        setShowSortByMenu(true);
    }

    const onSortByItemClick = (option) => {
        setSelectedSortByValue(option);
        queryParams.set('sort', option.value);
        setQueryParams(queryParams, { replace: true });
        getSortByDisplay();
        handleSort(option.value);
    }

    const isSortByItemSelected = (option) => {
        return selectedSortByValue && selectedSortByValue.value === option.value;
    }

    return (
        <Col className="sort-by-container" ref={sortByRef}>
            <div className="sort-by-input" onMouseOver={handleSortByMenuOnMouseOver}>
                <div className="sort-by-selected-value">
                    {sortByTextPlaceholder}<strong>{getSortByDisplay()}</strong>
                </div>
                <div className="sort-by-tools">
                    <div className="sort-by-tool">
                        <SlArrowDown />
                    </div>
                </div>
            </div>
            {
                showSortByMenu &&
                <div className="sort-by-menu">
                    {
                        sortByOptions.map((option) => {
                            return (
                                <div
                                    key={option.value}
                                    className={`sort-by-items ${isSortByItemSelected(option)} && "selected"`}
                                    onClick={() => { onSortByItemClick(option) }}
                                >
                                    {option.label}
                                </div>
                            );
                        })
                    }
                </div>
            }
        </Col>
    );
}

export default SortBy;