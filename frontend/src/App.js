import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import HomeScreen from './screens/HomeScreen';
import ProductSearchScreen from './screens/ProductSearchScreen';
import ProductScreen from './screens/ProductScreen';
import CartScreen from './screens/CartScreen';
import UserRegisterScreen from './screens/UserRegisterScreen';
import RouteWithNavbar from './RouteWithNavbar';
import RouteWithoutNavbar from './RouteWithoutNavbar';

function App() {

    return (
        <Router>
            <Routes>
                <Route element={<RouteWithoutNavbar />}>
                    <Route path='/user/register' element={<UserRegisterScreen />}/>
                </Route>
                <Route element={<RouteWithNavbar />} >
                    <Route path='/' element={<HomeScreen />} exact />
                    <Route path='/:slug' element={<ProductSearchScreen />}/>
                    <Route path='/products/:slug/:id/buy' element={<ProductScreen />} />
                    <Route path='/cart' element={<CartScreen />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
