// import React, { useEffect, useState } from 'react';
// import { useNavigate } from 'react-router-dom';
// import './CreateContract.css';

// function CreateContract() {
//   const [contractTitle, setContractTitle] = useState('');
//   const [contractDetails, setContractDetails] = useState('');
//   const [connections, setConnections] = useState([]);
//   const [searchTerm, setSearchTerm] = useState('');
//   const [selectedUser, setSelectedUser] = useState(null);
//   const navigate = useNavigate();

//   useEffect(() => {
//     const fetchConnections = async () => {
//       const token = localStorage.getItem('token');

//       if (!token) {
//         alert('You are not authenticated. Please log in.');
//         return;
//       }

//       try {
//         const response = await fetch('http://localhost:8000/api/v1/connections', {
//           method: 'GET',
//           headers: {
//             'Authorization': `Bearer ${token}`,
//             'Content-Type': 'application/json'
//           }
//         });

//         if (!response.ok) {
//           const errorResponse = await response.json();
//           throw new Error('Failed to fetch connections: ' + errorResponse.message);
//         }

//         const result = await response.json();
//         setConnections(result.connections);
//       } catch (error) {
//         alert(error.message);
//       }
//     };

//     fetchConnections();
//   }, []);

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     if (!selectedUser) {
//       alert('Please select a user to send an offer.');
//       return;
//     }

//     const offerData = {
//       contract_title: contractTitle,
//       contract_details: contractDetails,
//       user_id: selectedUser.connection_id
//     };

//     try {
//       const token = localStorage.getItem('token');
//       const response = await fetch('http://localhost:8000/api/v1/send-offer', {
//         method: 'POST',
//         headers: {
//           'Authorization': `Bearer ${token}`,
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(offerData)
//       });

//       if (!response.ok) {
//         const errorResponse = await response.json();
//         throw new Error('Failed to send offer: ' + errorResponse.message);
//       }

//       alert('Offer sent successfully!');
//       setContractTitle('');
//       setContractDetails('');
//       setSelectedUser(null);
//     } catch (error) {
//       alert(error.message);
//     }
//   };

//   const filteredConnection = connections.filter(connection => 
//     connection.friend_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
//     connection.friend_email.toLowerCase().includes(searchTerm.toLowerCase()) ||
//     connection.friend_phone.toLowerCase().includes(searchTerm.toLowerCase())
//   );

//   const toggleSelectUser = (connection) => {
//     if (selectedUser && selectedUser.connection_id === connection.connection_id) {
//       // Deselect the user if already selected
//       setSelectedUser(null);
//     } else {
//       // Select the user
//       setSelectedUser(connection);
//     }
//   };

//   return (
//     <div className="contract">
//       <h2>Make a Contract</h2>
//       <h3>Your Connections</h3>
//       <input
//         type="text"
//         placeholder="Search connections..."
//         value={searchTerm}
//         onChange={(e) => setSearchTerm(e.target.value)}
//         style={{ marginBottom: '10px', width: '100%' }}
//       />
//       <div style={{ maxHeight: '200px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
//         {filteredConnection.length > 0 ? (
//           <ul>
//             {filteredConnection.map((connection) => (
//               <li key={connection.connection_id}>
//                 {connection.friend_name} - {connection.friend_email} - {connection.friend_phone}
//                 <button onClick={() => toggleSelectUser(connection)} style={{ marginLeft: '10px' }}>
//                   {selectedUser && selectedUser.connection_id === connection.connection_id ? 'Deselect' : 'Select'}
//                 </button>
//                 {selectedUser && selectedUser.connection_id === connection.connection_id && (
//                   <span style={{ marginLeft: '10px', color: 'green' }}>✔️</span>
//                 )}
//               </li>
//             ))}
//           </ul>
//         ) : (
//           <p>No connections found.</p>
//         )}
//       </div>
//       <form onSubmit={handleSubmit}>
//         <label htmlFor="contractTitle">Contract Title:</label>
//         <input
//           type="text"
//           id="contractTitle"
//           name="contractTitle"
//           value={contractTitle}
//           onChange={(e) => setContractTitle(e.target.value)}
//           required
//         />

//         <label htmlFor="contractDetails">Contract Details:</label>
//         <textarea
//           id="contractDetails"
//           name="contractDetails"
//           value={contractDetails}
//           onChange={(e) => setContractDetails(e.target.value)}
//           required
//         ></textarea>

//         <button type="submit">Send Offer</button>
//       </form>
//     </div>
//   );
// }

// export default CreateContract; 

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreateContract.css';

function CreateContract() {
  const [connections, setConnections] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUser, setSelectedUser] = useState(null);
  const [selectedContractType, setSelectedContractType] = useState('');
  const [formData, setFormData] = useState({});
  const [showCustomizeFields, setShowCustomizeFields] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchConnections = async () => {
      const token = localStorage.getItem('token');

      if (!token) {
        alert('You are not authenticated. Please log in.');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/api/v1/connections', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          const errorResponse = await response.json();
          throw new Error('Failed to fetch connections: ' + errorResponse.message);
        }

        const result = await response.json();
        setConnections(result.connections);
      } catch (error) {
        alert(error.message);
      }
    };

    fetchConnections();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedUser) {
      alert('Please select a user to send an offer.');
      return;
    }

    const offerData = {
      user_id: selectedUser.connection_id,
      contract_type: selectedContractType,
    };

    // Set contract title and details based on contract type
    // if (selectedContractType === "CUSTOM CONTRACT") {
    //   offerData.contract_title = formData.custom_contract_title;
    //   offerData.contract_details = formData.custom_contract_details;
    // } else {
    //   offerData.contract_title = formData.agreement_name; // For other contract types

    // }

    // if (selectedContractType === "CUSTOM CONTRACT") {
    //   offerData.contract_title = formData.custom_contract_title;
    //   offerData.contract_details = {details: formData.custom_contract_details};
    //   offerData.contract_type = selectedContractType;
    // } else {
    //   offerData.contract_details = {
    //     amount: formData.amount,
    //     interest_rate: formData.interest_rate,
    //     duration: formData.duration,
    //     payment_mode: formData.payment_mode,
    //   };
    //   offerData.contract_title = formData.agreement_name;
    //   offerData.contract_type = selectedContractType;
    // }
    if (selectedContractType === "CUSTOM CONTRACT") {
      offerData.contract_title = formData.custom_contract_title;
      offerData.contract_details = { details: formData.custom_contract_details };
    } else {
      // For other contract types, gather all mandatory fields
      offerData.contract_title = formData.agreement_name; 
      offerData.contract_details = {
        amount: formData.amount,
        interest_rate: formData.interest_rate,
        duration: formData.duration,
        payment_mode: formData.payment_mode,
        // Add other fields as necessary based on the selected contract type
        ...(selectedContractType === "FRIENDLY LOAN AGREEMENT" && {
          late_interest_rate: formData.late_interest_rate,
          repayment_due_date: formData.repayment_due_date,
        }),
        ...(selectedContractType === "SALES AGREEMENT" && {
          product_name: formData.product_name,
          quantity: formData.quantity,
          price_per_unit: formData.price_per_unit,
          total_price: formData.total_price,
          delivery_days: formData.delivery_days,
        }),
        ...(selectedContractType === "CURRENCY EXCHANGE AGREEMENT" && {
          amount_sent: formData.amount_sent,
          currency_sent: formData.currency_sent,
          converted_amount: formData.converted_amount,
          currency_received: formData.currency_received,
        }),
        ...(selectedContractType === "SERVICE AGREEMENT" && {
          service_name: formData.service_name,
          completion_deadline: formData.completion_deadline,
          amount: formData.amount,
        }),
        ...(selectedContractType === "BARTER AGREEMENT" && {
          commodity_by_sender: formData.commodity_by_sender,
          commodity_by_receiver: formData.commodity_by_receiver,
        }),
      };
      // For other contract types
    }


    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/send-offer', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(offerData)
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error('Failed to send offer: ' + errorResponse.message);
      }

      alert('Offer sent successfully!');
      setSelectedUser(null);
      setSelectedContractType('');
      setFormData({});
      setShowCustomizeFields(false); // Reset customize fields visibility
    } catch (error) {
      alert(error.message);
    }
  };

  const filteredConnection = connections.filter(connection => 
    connection.friend_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    connection.friend_email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    connection.friend_phone.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleSelectUser = (connection) => {
    if (selectedUser && selectedUser.connection_id === connection.connection_id) {
      setSelectedUser(null);
    } else {
      setSelectedUser(connection);
    }
  };

  const handleContractTypeChange = (e) => {
    setSelectedContractType(e.target.value);
    setFormData({}); // Reset form data when changing contract type
    setShowCustomizeFields(false); // Reset customize fields visibility
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({ ...prevData, [name]: value }));
  };

  const renderMandatoryFields = () => {
    switch (selectedContractType) {
      case "LOAN AGREEMENT":
        return (
          <div>
            <label>Agreement Name:</label>
            <input type="text" name="agreement_name" onChange={handleInputChange} required />
            <label>Amount:</label>
            <input type="number" name="amount" onChange={handleInputChange} required />
            <label>Interest Rate:</label>
            <input type="number" name="interest_rate" onChange={handleInputChange} required />
            <label>Duration:</label>
            <input type="text" name="duration" onChange={handleInputChange} required />
            <label>Payment Mode:</label>
            <select name="payment_mode" onChange={handleInputChange} required>
              <option value="">Select Payment Mode</option>
              <option value="CASH">Cash</option>
              <option value="UPI/NEFT/RTGS">UPI/NEFT/RTGS</option>
            </select>
          </div>
        );
      case "FRIENDLY LOAN AGREEMENT":
        return (
          <div>
            <label>Agreement Name:</label>
            <input type="text" name="agreement_name" onChange={handleInputChange} required />
            <label>Amount:</label>
            <input type="number" name="amount" onChange={handleInputChange} required />
            <label>Payment Mode:</label>
            <select name="payment_mode" onChange={handleInputChange} required>
              <option value="">Select Payment Mode</option>
              <option value="CASH">Cash</option>
              <option value="UPI/NEFT/RTGS">UPI/NEFT/RTGS</option>
            </select>
          </div>
        );
      case "SALES AGREEMENT":
        return (
          <div>
            <label>Agreement Name:</label>
            <input type="text" name="agreement_name" onChange={handleInputChange} required />
            <label>Product Name:</label>
            <input type="text" name="product_name" onChange={handleInputChange} required />
            <label>Quantity:</label>
            <input type="number" name="quantity" onChange={handleInputChange} required />
            <label>Price per Unit:</label>
            <input type="number" name="price_per_unit" onChange={handleInputChange} required />
            <label>Total Price:</label>
            <input type="number" name="total_price" onChange={handleInputChange} required />
            <label>Payment Mode:</label>
            <select name="payment_mode" onChange={handleInputChange} required>
              <option value="">Select Payment Mode</option>
              <option value="CASH">Cash</option>
              <option value="UPI/NEFT/RTGS">UPI/NEFT/RTGS</option>
            </select>
          </div>
        );
      case "CURRENCY EXCHANGE AGREEMENT":
        return (
          <div>
            <label>Agreement Name:</label>
            <input type="text" name="agreement_name" onChange={handleInputChange} required />
            <label>Amount Sent:</label>
            <input type="number" name="amount_sent" onChange={handleInputChange} required />
            <label>Currency Sent:</label>
            <input type="text" name="currency_sent" onChange={handleInputChange} required />
            <label>Converted Amount:</label>
            <input type="number" name="converted_amount" onChange={handleInputChange} required />
            <label>Currency Received:</label>
            <input type="text" name="currency_received" onChange={handleInputChange} required />
          </div>
        );
      case "SERVICE AGREEMENT":
        return (
          <div>
            <label>Agreement Name:</label>
            <input type="text" name="agreement_name" onChange={handleInputChange} required />
            <label>Service Name:</label>
            <input type="text" name="service_name" onChange={handleInputChange} required />
            <label>Completion Deadline:</label>
            <input type="date" name="completion_deadline" onChange={handleInputChange} required />
            <label>Payment Mode:</label>
            <select name="payment_mode" onChange={handleInputChange} required>
              <option value="">Select Payment Mode</option>
              <option value="CASH">Cash</option>
              <option value="UPI/NEFT/RTGS">UPI/NEFT/RTGS</option>
            </select>
            <label>Amount:</label>
            <input type="number" name="amount" onChange={handleInputChange} required />
          </div>
        );
      case "BARTER AGREEMENT":
        return (
          <div>
            <label>Agreement Name:</label>
            <input type="text" name="agreement_name" onChange={handleInputChange} required />
            <label>Commodity by Sender:</label>
            <input type="text" name="commodity_by_sender" onChange={handleInputChange} required />
            <label>Commodity by Receiver:</label>
            <input type="text" name="commodity_by_receiver" onChange={handleInputChange} required />
          </div>
        );
      case "CUSTOM CONTRACT":
        return null; // No mandatory fields for custom contract
      default:
        return null;
    }
  };

  const renderCustomizeFields = () => {
    switch (selectedContractType) {
      case "LOAN AGREEMENT":
        return (
          <div>
            <label>Repayment Type:</label>
            <input type="text" name="repayment_type" onChange={handleInputChange} />
            <label>Penalty Applied After Days:</label>
            <input type="number" name="penalty_days" onChange={handleInputChange} />
            <label>Jurisdiction:</label>
            <input type="text" name="jurisdiction" onChange={handleInputChange} />
            <label>Arbitrator:</label>
            <input type="text" name="arbitrator" onChange={handleInputChange} />
          </div>
        );
      case "FRIENDLY LOAN AGREEMENT":
        return (
          <div>
            <label>Interest Rate:</label>
            <input type="number" name="interest_rate" onChange={handleInputChange} />
            <label>Late Interest Rate:</label>
            <input type="number" name="late_interest_rate" onChange={handleInputChange} />
            <label>Repayment Due Date:</label>
            <input type="date" name="repayment_due_date" onChange={handleInputChange} />
            <label>Jurisdiction:</label>
            <input type="text" name="jurisdiction" onChange={handleInputChange} />
            <label>Arbitrator:</label>
            <input type="text" name="arbitrator" onChange={handleInputChange} />
          </div>
        );
      case "SALES AGREEMENT":
        return (
          <div>
            <label>Delivery Days:</label>
            <input type="number" name="delivery_days" onChange={handleInputChange} />
            <label>Jurisdiction:</label>
            <input type="text" name="jurisdiction" onChange={handleInputChange} />
            <label>Clauses:</label>
            <textarea name="clauses" onChange={handleInputChange}></textarea>
          </div>
        );
      case "CURRENCY EXCHANGE AGREEMENT":
        return (
          <div>
            <label>Jurisdiction:</label>
            <input type="text" name="jurisdiction" onChange={handleInputChange} />
          </div>
        );
      case "SERVICE AGREEMENT":
        return (
          <div>
            <label>Jurisdiction:</label>
            <input type="text" name="jurisdiction" onChange={handleInputChange} />
            <label>Additional Details:</label>
            <textarea name="additional_details" onChange={handleInputChange}></textarea>
          </div>
        );
      case "BARTER AGREEMENT":
        return (
          <div>
            <label>Jurisdiction:</label>
            <input type="text" name="jurisdiction" onChange={handleInputChange} />
            <label>Additional Details:</label>
            <textarea name="additional_details" onChange={handleInputChange}></textarea>
          </div>
        );
      case "CUSTOM CONTRACT":
        return (
          <div>
            <label>Contract Title:</label>
            <input type="text" name="custom_contract_title" onChange={handleInputChange} required />
            <label>Contract Details:</label>
            <textarea name="custom_contract_details" onChange={handleInputChange} required></textarea>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="contract">
      <h2>Make a Contract</h2>
      <h3>Your Connections</h3>
      <input
        type="text"
        placeholder="Search connections..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ marginBottom: '10px', width: '100%' }}
      />
      <div style={{ maxHeight: '200px', overflowY: 'scroll', border: '1px solid #ccc', padding: '10px' }}>
        {filteredConnection.length > 0 ? (
          <ul>
            {filteredConnection.map((connection) => (
              <li key={connection.connection_id}>
                {connection.friend_name} - {connection.friend_email} - {connection.friend_phone}
                <button onClick={() => toggleSelectUser(connection)} style={{ marginLeft: '10px' }}>
                  {selectedUser && selectedUser.connection_id === connection.connection_id ? 'Deselect' : 'Select'}
                </button>
                {selectedUser && selectedUser.connection_id === connection.connection_id && (
                  <span style={{ marginLeft: '10px', color: 'green' }}>✔️</span>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>No connections found.</p>
        )}
      </div>
      <form onSubmit={handleSubmit}>
        <label htmlFor="contractType">Select Contract Type:</label>
        <select
          id="contractType"
          value={selectedContractType}
          onChange={handleContractTypeChange}
          required
        >
          <option value="">--Select a Contract Type--</option>
          <option value="LOAN AGREEMENT">Loan Agreement</option>
          <option value="FRIENDLY LOAN AGREEMENT">Friendly Loan Agreement</option>
          <option value="SALES AGREEMENT">Sales Agreement</option>
          <option value="CURRENCY EXCHANGE AGREEMENT">Currency Exchange Agreement</option>
          <option value="SERVICE AGREEMENT">Service Agreement</option>
          <option value="BARTER AGREEMENT">Barter Agreement</option>
          <option value="CUSTOM CONTRACT">Create Custom Contract</option>
        </select>

        {selectedContractType && renderMandatoryFields()}

        {selectedContractType && selectedContractType !== "CUSTOM CONTRACT" && (
          <button type="button" onClick={() => setShowCustomizeFields(!showCustomizeFields)}>
            {showCustomizeFields ? 'Hide Customize Fields' : 'Show Customize Fields'}
          </button>
        )}

        {showCustomizeFields && renderCustomizeFields()}

        {selectedContractType === "CUSTOM CONTRACT" && (
          <div>
            <label>Contract Title:</label>
            <input type="text" name="custom_contract_title" onChange={handleInputChange} required />
            <label>Contract Details:</label>
            <textarea name="custom_contract_details" onChange={handleInputChange} required></textarea>
          </div>
        )}

        <button type="submit">Send Offer</button>
      </form>
    </div>
  );
}

export default CreateContract;
