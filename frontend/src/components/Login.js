import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!email || !password) {
      alert('Email and password are required.');
      return;
    }

    const data = new URLSearchParams();
    data.append('username', email);
    data.append('password', password);

    console.log('Sending data:', data.toString());

    try {
      const response = await fetch('http://localhost:8000/api/v1/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: data.toString()
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        console.error('Error response:', errorResponse);
        throw new Error('Login failed: ' + errorResponse.message);
      }

      const result = await response.json();
      alert(result.message);
      localStorage.setItem('token', result.token);

      navigate('/user');
    } catch (error) {
      alert(error.message);
    }
  };

  const handleSignUp = () => {
    navigate('/signup'); // Navigate to the Sign Up page
  };

  return (
    <div className="login">
      <h2>Login</h2>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={handleLogin}>Login</button>
      <div className="signup-link">
        <p>Don't have an account?</p>
        <button onClick={handleSignUp}>Sign Up</button>
      </div>
    </div>
  );
}

export default Login;