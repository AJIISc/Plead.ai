// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import CreateContract from './components/CreateContract';
import Help from './components/Help';
import Chatbot from './components/Chatbot';
import PaymentComponent from './components/PaymentComponent';
import LegalCounselComponent from './components/LegalCounselComponent';
import SignupComponent from './components/SignupComponent';
import ForgotPasswordComponent from './components/ForgotPasswordComponent';
import UserPage from './components/UserPage';
import PendingContracts from './components/PendingContracts';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/create-contract" element={<CreateContract />} />
          <Route path="/help" element={<Help />} />
          <Route path="/payment" element={<PaymentComponent />} />
          <Route path="/legal-counsel" element={<LegalCounselComponent />} />
          <Route path="/signup" element={<SignupComponent />} />
          <Route path="/forgot-password" element={<ForgotPasswordComponent />} />
          <Route path="/user" element={<UserPage />} />
          <Route path="/contracts/pending" element={<PendingContracts />} />
        </Routes>
        <Chatbot />
      </div>
    </Router>
  );
}

export default App;