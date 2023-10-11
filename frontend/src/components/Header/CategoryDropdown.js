import "../../css/Header/CategoryDropdown.css";

import { NavDropdown } from "react-bootstrap";
import React from "react";
import { useSelector } from "react-redux";

// import categories from "../../categories";

function CategoryDropdown() {
    
    const categoryList = useSelector(state => state.categoryList)
    const { categories } = categoryList
    
    return (
        <>
        {
            categories?.map((parentCategory, parentIndex) => {
                return (
                    <NavDropdown 
                        title={parentCategory.name}
                        key={parentIndex}
                        className="category-dropdown-level-1"
                    >
                        <div className="category-dropdown-level-2">
                        {
                            parentCategory?.children.map((category, categoryIndex) => {
                                return (
                                    // Adding a div will cause break of code but key prop cannot be added to <></>
                                    // React.Fragment is same as <></> and allows to add key prop as well.
                                    <React.Fragment key={categoryIndex}>
                                        <NavDropdown.Header>
                                            <a href={category.slug}>
                                                {category.name}
                                            </a>
                                        </NavDropdown.Header>
                                        {
                                            category?.children.map((subCategory, subCategoryIndex) => {
                                                return (
                                                    <NavDropdown.Item 
                                                        key={subCategoryIndex} 
                                                        className="category-dropdown-level-3"
                                                        href={subCategory.slug}
                                                    >
                                                        {subCategory.name}
                                                    </NavDropdown.Item>
                                                )
                                            })
                                        }
                                        <NavDropdown.Divider className="dropdown-divider"/>
                                    </React.Fragment>
                                )
                            })
                        }
                        </div>
                    </NavDropdown>
                )
            })
        }
        </>
    );
}

export default CategoryDropdown;