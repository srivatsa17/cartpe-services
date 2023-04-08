import { Container } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
    return (
        <div>
            <Header />
            <main className='py-3'>
                <Container>
                    <h1>Hello, Welcome</h1>
                </Container>
            </main>
            <hr/>
            <Footer />
        </div>
    );
}

export default App;
