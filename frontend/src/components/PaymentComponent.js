import React from 'react';

const PaymentComponent = () => {
    return (
        <div className="payment-component" style={{ color: '#ADD8E6', backgroundColor: '#121212' }}>
            <h2 style={{ color: '#4682B4' }}>Make a Payment</h2>
            <input type="text" placeholder="Enter amount" style={{ backgroundColor: '#A9A9A9', color: '#000000', padding: '10px', borderRadius: '5px', border: 'none', marginBottom: '10px' }} />
            <button style={{ color: '#ADD8E6', backgroundColor: '#1a1a1a' }}>Pay Now</button>
        </div>
    );
};

export default PaymentComponent; 