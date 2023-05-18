import React, { useEffect, useState, useRef } from "react";
import { Col } from 'react-bootstrap';
import { SlArrowDown } from 'react-icons/sl';
import '../../css/ProductSearchScreen/SortBy.css';

function SortBy() {
    const sortByRef = useRef(null);
    const [showSortByMenu, setShowSortByMenu] = useState(false);
    const [selectedSortByValue, setSelectedSortByValue] = useState(null);

    const sortByTextPlaceholder = "Sort By: ";

    const sortByOptions = [
        { value : "What's New", label : "What's New"},
        { value : "Popularity", label : "Popularity"},
        { value : "Better discount", label : "Better discount"},
        { value : "Price: High to Low", label : "Price: High to Low"},
        { value : "Price: Low to High", label : "Price: Low to High"},
        { value : "Customer Rating", label : "Customer Rating"}
    ]

    const getSortByDisplay = () => {
        if(selectedSortByValue) {
            return selectedSortByValue.label;
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
        getSortByDisplay();
    }

    const isSortByItemSelected = (option) => {
        if(! selectedSortByValue) {
            return false;
        }
        return selectedSortByValue.value === option.value;
    }

    return (
        <Col className="sort-by-container" ref={sortByRef}>
            <div className="sort-by-input" onMouseOver={handleSortByMenuOnMouseOver}>
                <div className="sort-by-selected-value">
                    {sortByTextPlaceholder}<strong>{ getSortByDisplay() }</strong>
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