import React from "react";
import '../../../css/ProductSearchScreen/Filters/FilterButtonToggle.css';

function FilterButtonToggle({ visible, active, onApply, onClear }) {
    if(active) {
        return (
            <button 
                className="filter-button clear" 
                type="submit" 
                onClick={onClear} 
                disabled={!active}
            >
                Clear
            </button>
        )
    }
    
    if(visible) {
        return (
            <button 
                className="filter-button apply" 
                type="submit" 
                onClick={onApply} 
                disabled={!visible}
            >
                Apply
            </button>
        )
    }
}

export default FilterButtonToggle;