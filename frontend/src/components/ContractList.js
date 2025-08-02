// frontend/src/components/ContractList.js
import React, { useEffect, useState } from 'react';
import axios from '../services/api';

function ContractList() {
  const [contracts, setContracts] = useState([]);

  useEffect(() => {
    axios.get('/contracts/')
      .then(response => setContracts(response.data))
      .catch(error => console.error('Error fetching contracts:', error));
  }, []);

  return (
    <div>
      <h2>Contracts</h2>
      <ul>
        {contracts.map(contract => (
          <li key={contract.id}>{contract.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default ContractList;