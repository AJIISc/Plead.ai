import React, { useState } from 'react';

const ForgotPasswordComponent = () => {
    const [email, setEmail] = useState('');

    const handlePasswordReset = (e) => {
        e.preventDefault();
        // Add logic to send encrypted password reset link to user's email
        console.log('Password reset link sent to:', email);
    };

    return (
        <div className="forgot-password-component" style={{ maxWidth: '400px', margin: '0 auto', padding: '20px', border: '1px solid #ccc', borderRadius: '10px' }}>
            <h2>Forgot Password</h2>
            <form onSubmit={handlePasswordReset} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <button type="submit">Send Reset Link</button>
            </form>
        </div>
    );
};

export default ForgotPasswordComponent; 