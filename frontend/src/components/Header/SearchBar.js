import '../../css/Header/SearchBar.css';

import React, { useEffect, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { FaSearch } from 'react-icons/fa';
import { GrClose } from 'react-icons/gr';
import { Link } from "react-router-dom";
import { getSearchedCategories } from '../../actions/productActions';

function SearchBar() {

    const [searchText, setSearchText] = useState("");
    const [showSearchResult, setShowSearchResult] = useState(false);
    const searchResultsRef = useRef(null);
    const dispatch = useDispatch()
    const categoryList = useSelector(state => state.searchedCategories)
    var { categories, error } = categoryList

    const handleInputChange = (event) => {
        const inputValue = event.target.value.toLowerCase().trim();
        if (inputValue === "") {
            setSearchText("");
        } else {
            setSearchText(inputValue);
            if(inputValue.length > 2) {
                dispatch(getSearchedCategories(inputValue))
                if(!error) {
                    setShowSearchResult(true)
                }
            }
        }
    };

    const clearSearchInput = () => {
        setShowSearchResult(false);
        setSearchText("");
    };

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (searchResultsRef.current && !searchResultsRef.current.contains(event.target)) {
                clearSearchInput();
            }
        };
        // add event listener to detect clicks outside of the search component
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [searchResultsRef]);

    return (
        <div className="searchContainer">
            <div className="searchInputs">
                <input
                    type="search"
                    placeholder="Search for a product"
                    value={searchText}
                    onChange={handleInputChange}
                />
                <div>
                    {
                        ! searchText.length ? (
                            <FaSearch className="searchIcon"/>
                        ) : (
                            <GrClose className="searchIcon" id="clearButton" onClick={clearSearchInput}/>
                        )
                    }
                </div>
            </div>
            {
                showSearchResult && categories && categories.length !== 0 && (
                    <div className="searchResults" ref={searchResultsRef}>
                    {
                        categories.map((category, index) => {
                            return (
                                <Link
                                    to={{ pathname: `/${category.slug}`, search: `searchItem=${category.name}`}}
                                    state={{ resetSortTitle: true }}
                                    className="searchItem"
                                    key={index}
                                    onClick={clearSearchInput}
                                >
                                    {category.name}
                                </Link>
                            )
                        })
                    }
                    </div>
                )
            }
        </div>
    );
}

export default SearchBar;