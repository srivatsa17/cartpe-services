import React, { useState, useRef, useEffect } from 'react';
import { Link } from "react-router-dom";
import { FaSearch } from 'react-icons/fa';
import { GrClose } from 'react-icons/gr';
import categories from "../../products";
import '../../css/Header/SearchBar.css';

function SearchBar() {

    const [filteredData, setFilteredData] = useState([]);
    const [searchText, setSearchText] = useState("");
    const searchRef = useRef(null);
    const temp_arr = []
    
    function recursiveCall(categories) {
        categories.forEach((category) => {
            if(category.children.length) {
                recursiveCall(category.children)
            }
            if(category.level !== 0) {
                temp_arr.push(category)
            }
        })
        return temp_arr
    }
    
    const categoriesList = recursiveCall(categories);
    console.log(categoriesList);

    const handleInputChange = (event) => {
        const inputValue = event.target.value.toLowerCase().trim();
        if (inputValue === "") {
            setSearchText("");
            setFilteredData([]);
        } else {
            setSearchText(inputValue);
            const filter = categoriesList.filter((category) => {
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
            if (searchRef.current && !searchRef.current.contains(event.target)) {
                clearSearchInput();
            }
        };
        // add event listener to detect clicks outside of the search component
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [searchRef]);

    return (
        <div className="searchContainer">
            <div className="searchInputs">
                <input
                    type="search"
                    placeholder="Search for a product"
                    value={searchText}
                    onChange={handleInputChange}
                />
                {
                    ! searchText.length ? (
                        <FaSearch className="searchIcon"/>
                    ) : (
                        <GrClose className="searchIcon" id="clearButton" onClick={clearSearchInput}/>
                    )
                }
            </div>
            {
                filteredData.length !== 0 && (
                    <div className="searchResults" ref={searchRef}>
                    {
                        filteredData.map((category, index) => {
                            return (
                                <Link
                                    to={`/product/${category.slug}`}
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