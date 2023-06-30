import '../../../css/ProductSearchScreen/SortBy/SortByMenu.css'

import React from 'react';

function SortByMenu({ showSortByMenu, handleSortByItemClick, sortByOptions }) {

    return (
        <>
            {
                showSortByMenu &&
                <div className="sort-by-menu">
                    {
                        sortByOptions.map((option) => {
                            return (
                                <div
                                    key={option.value}
                                    className="sort-by-items"
                                    onClick={() => { handleSortByItemClick(option) }}
                                >
                                    {option.label}
                                </div>
                            );
                        })
                    }
                </div>
            }
        </>
    )
}

export default SortByMenu;