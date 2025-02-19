
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Form, ProgressBar, Spinner, Alert, Row, Col, Card } from 'react-bootstrap';

function TrainingProgress() {
    const [epochs, setEpochs] = useState(10);
    const [userId, setUserId] = useState('user1');
    const [progress, setProgress] = useState(0);
    const [currentEpoch, setCurrentEpoch] = useState('');
    const [status, setStatus] = useState('');
    const [isTraining, setIsTraining] = useState(false);
    const [timeTaken, setTimeTaken] = useState('');
    const [metrics, setMetrics] = useState({});

    const startTraining = async () => {
        console.log('Starting training... with epochs:', epochs);
        setIsTraining(true);
        setStatus('');
        setProgress(0);
        setCurrentEpoch('');
        setTimeTaken('');
        setMetrics({});
        await axios.post('http://localhost:8082/train', { epochs, user_id: userId });
    };

    useEffect(() => {
        const eventSource = new EventSource(`http://localhost:8082/progress/${userId}`);
        eventSource.onmessage = (event) => {
            const message = event.data.trim(); // Trim whitespace
            if (message.startsWith('progress:')) {
                const [progressPart, epochPart] = message.split(',');
                setProgress(parseFloat(progressPart.split(':')[1]));
                setCurrentEpoch(epochPart.split(':')[1]);
            } else {
                try {
                    const data = JSON.parse(message);
                    if (data.status === 'completed') {
                        setStatus('completed');
                        setTimeTaken(data.time_taken);
                        setMetrics(data.metrics);
                        setIsTraining(false);
                    }
                } catch (error) {
                    console.error('Error parsing message:', error);
                }
            }
        };
        return () => {
            eventSource.close();
        };
    }, [userId]);

    return (
        <Card className="p-4 shadow mx-auto" style={{ maxWidth: '600px', textAlign: 'center' }}>
            <Form>
                <Row className="mb-3">
                    <Col md={8} className="mx-auto">
                        <Form.Group controlId="formEpochs">
                            <Form.Label>Number of Epochs</Form.Label>
                            <Form.Control
                                type="number"
                                value={epochs}
                                onChange={(e) => setEpochs(e.target.value)}
                                disabled={isTraining}
                                className="text-center"
                            />
                        </Form.Group>
                    </Col>
                </Row>
                <Row>
                    <Col md={8} className="mx-auto">
                        <Button variant="primary" onClick={startTraining} disabled={isTraining} className="w-100">
                            {isTraining ? (
                                <>
                                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> Training...
                                </>
                            ) : (
                                'Start Training'
                            )}
                        </Button>
                    </Col>
                </Row>
            </Form>
            {isTraining && (
                <>
                    <div className="mt-4">
                        <ProgressBar animated now={progress} label={`${progress}%`} />
                    </div>
                    <div className="mt-2">
                        <h5>{currentEpoch}</h5>
                    </div>
                </>
            )}
            {status && (
                <Alert variant={status.toLowerCase() === 'completed' ? 'success' : 'danger'} className="mt-4">
                    {status.toLowerCase() === 'completed' ? (
                        <>
                            <p>Training Completed!</p>
                            <p>Time Taken: {timeTaken}</p>
                            <h5>Metrics:</h5>
                            <ul>
                                {Object.entries(metrics).map(([key, value]) => (
                                    <li key={key}>{key}: {value.toFixed(2) * 100} %</li>
                                ))}
                            </ul>
                        </>
                    ) : (
                        `Error: ${status}`
                    )}
                </Alert>
            )}
        </Card>
    );
}

export default TrainingProgress;