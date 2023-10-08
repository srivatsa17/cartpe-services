import '../../css/Header/SearchBar.css';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import { FaSearch } from 'react-icons/fa';
import { GrClose } from 'react-icons/gr';
import { Link } from "react-router-dom";
import { debounce } from 'lodash';
import { getSearchedCategories } from '../../actions/productActions';

function SearchBar() {
    const [searchText, setSearchText] = useState("");
    const [showSearchResult, setShowSearchResult] = useState(false);
    const searchResultsRef = useRef(null);
    const dispatch = useDispatch()
    const categoryList = useSelector(state => state.searchedCategories)
    var { categories, error } = categoryList

    const debouncedSendRequest = useMemo(() => {
        const sendRequest = (searchText) => {
            dispatch(getSearchedCategories(searchText))
        };
            
        return debounce(sendRequest, 400);
    }, [dispatch]);
      
    const handleInputChange = (event) => {
        const inputValue = event.target.value.toLowerCase();
        if (inputValue === "") {
            setSearchText("");
        } else {
            setSearchText(inputValue);
            if(inputValue.trim().length > 2) {
                debouncedSendRequest(inputValue.trim())
                setShowSearchResult(true)
            } else {
                setShowSearchResult(false)
            }
        }
    };

    const clearSearchInput = () => {
        setSearchText("");
    };

    const hideSearchResults = () => {
        setShowSearchResult(false);
    }

    const clearSearchResults = () => {
        setSearchText("");
        setShowSearchResult(false);
    }

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (searchResultsRef.current && !searchResultsRef.current.contains(event.target)) {
                hideSearchResults();
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
            
            <div ref={searchResultsRef}>
                {
                    showSearchResult && (
                        error || ! categories ? (
                            <div className="searchResults">
                                <div className="searchItem noResultFound">
                                    Something went wrong!
                                </div>
                            </div>
                        ) : (
                            categories.length === 0 ? (
                                <div className="searchResults">
                                    <div className="searchItem noResultFound">
                                        Oops, no results found!
                                    </div>
                                </div>
                            ) : (
                                <div className="searchResults">
                                {
                                    categories.map((category, index) => {
                                        return (
                                            <Link
                                                to={{   
                                                    pathname: `/${category.slug}`, 
                                                    search: `searchItem=${category.name}`
                                                }}
                                                state={{ resetSortTitle: true }}
                                                className="searchItem"
                                                key={index}
                                                onClick={clearSearchResults}
                                            >
                                                {category.name}
                                            </Link>
                                        )
                                    })
                                }
                                </div>
                            )
                        )
                    )
                }
            </div>
        </div>
    );
}

export default SearchBar;