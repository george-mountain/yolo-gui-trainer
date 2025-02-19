
import React from 'react';
import { Container, Navbar, Nav } from 'react-bootstrap';

const Layout = ({ children }) => {
    return (
        <div className="main-container">
            {/* Navbar */}
            <Navbar bg="dark" variant="dark" expand="lg">
                <Container>
                    <Navbar.Brand href="#">Model Training GUI</Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto">
                            <Nav.Link href="#">Home</Nav.Link>
                            <Nav.Link href="#">About</Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>

            {/* Centered Content */}
            <Container fluid className="d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
                <div className="training-card p-5 shadow-lg rounded bg-light text-center" style={{ width: '90%', maxWidth: '1200px' }}>
                    {children}
                </div>
            </Container>

            {/* Footer */}
            <footer className="bg-dark text-white text-center py-3">
                <Container>
                    <p className="mb-0">© 2025 Model Training GUI. All rights reserved.</p>
                </Container>
            </footer>
        </div>
    );
};

export default Layout;
