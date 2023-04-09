import { Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import HomeScreen from './screens/HomeScreen';

function App() {
    return (
        <div>
            <Header />
            <main className='py-3'>
                <Container>
                    <HomeScreen />
                </Container>
            </main>
            <hr/>
            <Footer />
        </div>
    );
}

export default App;
