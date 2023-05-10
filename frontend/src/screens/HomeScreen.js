import React from "react";
import { Row, Col } from "react-bootstrap";
import products from "../products";
import Product from "../components/Product";

function HomeScreen({ searchText }) {

    const filteredData = products.filter((originalData) => {
        if(searchText === "" || searchText === null) {
            return originalData;
        } else {
            return originalData.name.toLowerCase().includes(searchText);
        }
    })

    return (
        <div>
            <Row>
                {
                    filteredData.length ?
                    filteredData.map((product) => (
                        <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                            <Product product={product} />
                        </Col>
                    )) :
                    <h2>
                        <center>
                            Oops! Looks like your searched item is not found
                        </center>
                    </h2>
                }
            </Row>
        </div>
    );
}

export default HomeScreen;