import React, { useState, useRef, useEffect } from 'react';
import { Link } from "react-router-dom";
import { FaSearch } from 'react-icons/fa';
import { GrClose } from 'react-icons/gr';
import categories from "../../categories";
import '../../css/Header/SearchBar.css';

function getCategoriesList( categoriesSearchList, categories ) {
    categories.map((category) => {
        if(category.children.length > 0) {
            getCategoriesList(categoriesSearchList, category.children)
        }
        if(category.level !== 0) {
            categoriesSearchList.push(category)
        }
        return categoriesSearchList
    })
}

function SearchBar() {

    const [filteredData, setFilteredData] = useState([]);
    const [searchText, setSearchText] = useState("");
    const searchResultsRef = useRef(null);
    const categoriesSearchList = []

    useEffect(() => {
        getCategoriesList(categoriesSearchList, categories);
    })

    const handleInputChange = (event) => {
        const inputValue = event.target.value.toLowerCase().trim();
        if (inputValue === "") {
            setSearchText("");
            setFilteredData([]);
        } else {
            setSearchText(inputValue);
            const filter = categoriesSearchList?.filter((category) => {
                return category.name.toLowerCase().includes(inputValue);
            })
            setFilteredData(filter);
        }
    };

    const clearSearchInput = () => {
        setFilteredData([]);
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
                filteredData.length !== 0 && (
                    <div className="searchResults" ref={searchResultsRef}>
                    {
                        filteredData.map((category, index) => {
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