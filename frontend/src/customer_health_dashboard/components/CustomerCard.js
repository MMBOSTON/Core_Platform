import React from 'react';

const CustomerCard = ({ customerId, healthScore, npsScore, cesScore, signupDate, name, email }) => {
    return (
        <div className="customer-card">
            <h2>{name}</h2>
            <p>ID: {customerId}</p>
            <p>Email: {email}</p>
            <p>Sign-Up Date: {signupDate}</p>
            <p>NPS Score: {npsScore}</p>
            <p>CES Score: {cesScore}</p>
            <p>Health Score: {healthScore}</p>
        </div>
    );
};

export default CustomerCard;
