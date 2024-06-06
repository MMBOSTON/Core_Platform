import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CustomerCard from './CustomerCard';
import CustomerNPSChart from './CustomerNPSChart'; // Make sure this path is correct

const Dashboard = () => {
    const [healthScores, setHealthScores] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/customers')
        .then(response => setHealthScores(response.data))
        .catch(error => console.error('Error fetching health scores', error));
    }, []);

    return (
        <div className="dashboard">
            <h1>Customer Health Dashboard</h1>
            {healthScores.length > 0? (
                <>
                    {healthScores.map(score => (
                        <CustomerCard
                            key={score.customer_id}
                            customerId={score.customer_id}
                            usageFrequency={score.usage_frequency}
                            supportTickets={score.support_tickets}
                            npsScore={score.nps_score}
                        />
                    ))}
                    <CustomerNPSChart data={healthScores} />
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Dashboard;