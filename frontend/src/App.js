import React from 'react';
import { Container } from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './components/Header/Navbar';
import Footer from './components/Footer';
import HomeScreen from './screens/HomeScreen';
import ProductSearchScreen from './screens/ProductSearchScreen';
import ProductScreen from './screens/ProductScreen';
import CartScreen from './screens/CartScreen';

function App() {

    return (
        <Router>
            <Navbar />
            <main className='py-3'>
                <Container>
                    <Routes>
                        <Route path='/' element={<HomeScreen />} exact />
                        <Route path='/:slug' element={<ProductSearchScreen />}/>
                        <Route path='/products/:slug/:id/buy' element={<ProductScreen />} />
                        <Route path='/cart' element={<CartScreen />} />
                    </Routes>
                </Container>
            </main>
            <hr/>
            <Footer />
        </Router>
    );
}

export default App;
