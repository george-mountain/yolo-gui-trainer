

import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Layout from './Layout';
import TrainingProgress from './TrainingProgress';
import './styles.css'; 

function App() {
    return (
        <Layout>
            <h3 className="text-center mb-4">Model Training Progress</h3>
            <TrainingProgress />
        </Layout>
    );
}

export default App;

