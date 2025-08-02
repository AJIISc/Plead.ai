import React from 'react';

const LegalCounselComponent = () => {
    return (
        <div className="legal-counsel-component" style={{ color: '#ADD8E6', backgroundColor: '#121212' }}>
            <h2 style={{ color: '#4682B4' }}>Legal Counsel Options</h2>
            <div className="legal-opinion-section">
                <h3 style={{ color: '#4682B4' }}>Request Legal Opinion</h3>
                <input type="text" placeholder="Enter details" style={{ backgroundColor: '#A9A9A9', color: '#000000', padding: '10px', borderRadius: '5px', border: 'none', marginBottom: '10px' }} />
                <button style={{ color: '#ADD8E6', backgroundColor: '#1a1a1a' }}>Request Legal Opinion</button>
            </div>
            <div className="arbitrator-section">
                <h3 style={{ color: '#4682B4' }}>Get an Arbitrator</h3>
                <input type="text" placeholder="Enter details" style={{ backgroundColor: '#A9A9A9', color: '#000000', padding: '10px', borderRadius: '5px', border: 'none', marginBottom: '10px' }} />
                <button style={{ color: '#ADD8E6', backgroundColor: '#1a1a1a' }}>Request Arbitrator</button>
            </div>
        </div>
    );
};

export default LegalCounselComponent; 