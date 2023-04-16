import React, { useState } from 'react';
import { Container } from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header';
import Footer from './components/Footer';
import HomeScreen from './screens/HomeScreen';
import ProductScreen from './screens/ProductScreen';

function App() {
    // Searching for product in Header component as an event change and sending it as a prop to HomeScreen.
    // It is sent from here as we are communicating from parent to child component.
    const [searchText, setSearchText] = useState("");
    var handleChange = (event) => {
        setSearchText(event.target.value.toLowerCase());
    };

    return (
        <Router>
            <Header searchText={handleChange}/>
            <main className='py-3'>
                <Container>
                    <Routes>
                        <Route path='/' element={<HomeScreen searchText={searchText} />} exact />
                        <Route path='/product/:id' element={<ProductScreen />} />
                    </Routes>
                </Container>
            </main>
            <hr/>
            <Footer />
        </Router>
    );
}

export default App;
