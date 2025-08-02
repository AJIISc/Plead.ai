import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './UserPage.css';
import PendingContracts from './PendingContracts';

function UserPage() {
  const [identifier, setIdentifier] = useState(''); // For email or phone number
  const navigate = useNavigate();

  const handleSignOut = () => {
    localStorage.removeItem('token'); // Optionally remove the token on sign out
    navigate('/'); // Redirect to home page
  };

  const addConnection = async (e) => {
    e.preventDefault(); // Prevent default form submission

    const token = localStorage.getItem('token'); // Retrieve the token from localStorage

    if (!token || token === 'undefined') {
      alert('You are not authenticated. Please log in.');
      return;
    }

    const connectionData = { identifier }; // Prepare data to send

    try {
      const response = await fetch('http://localhost:8000/api/v1/connections', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`, // Include the token in the Authorization header
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(connectionData) // Send the connection data
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error('Failed to add connection: ' + errorResponse.message);
      }

      const result = await response.json();
      alert('Connection added successfully: ' + result.message);
      setIdentifier(''); // Reset the input field
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div className="user-page">
      <h2>User Dashboard</h2>
      <nav>
        <ul>
          <li><Link to="/home">Home</Link></li>
          <li><Link to="/create-contract">Create Contract</Link></li>
          <li>
            <div className="dropdown">
              <button className="dropbtn">Contracts</button>
              <div className="dropdown-content">
                <Link to="/contracts/pending">Pending Contracts</Link>
                <Link to="/contracts/active">Active Contracts</Link>
                <Link to="/contracts/counter-offer">Counter Offer Contracts</Link>
              </div>
            </div>
          </li>
          <li><Link to="/legal-counsel">Associated Legal Counsel</Link></li>
          <li><Link to="/help">Help</Link></li>
          <li><button onClick={handleSignOut}>Sign Out</button></li>
        </ul>
      </nav>

      <h3>Create Connection</h3>
      <form onSubmit={addConnection}>
        <label htmlFor="identifier">Friend Name, Email, or Phone Number:</label>
        <input
          type="text"
          id="identifier"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          required
        />
        <button type="submit">Add Connection</button>
      </form>

      <PendingContracts />
    </div>
  );
}

export default UserPage;