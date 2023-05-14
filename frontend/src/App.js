import React from 'react';
import { Container } from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './components/Header/Navbar';
import Footer from './components/Footer';
import HomeScreen from './screens/HomeScreen';
import ProductScreen from './screens/ProductScreen';

function App() {

    return (
        <Router>
            <Navbar />
            <main className='py-3'>
                <Container>
                    <Routes>
                        <Route path='/' element={<HomeScreen />} exact />
                        <Route path='/product/:slug' element={<ProductScreen />} />
                    </Routes>
                </Container>
            </main>
            <hr/>
            <Footer />
        </Router>
    );
}

export default App;
