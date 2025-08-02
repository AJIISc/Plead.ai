import React, { useState } from 'react';

const SignupComponent = () => {
    const [name, setName] = useState('');
    const [phone, setPhone] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [address, setAddress] = useState('');
    const [customerType, setCustomerType] = useState('individual');
    const [role, setRole] = useState('customer');  // New state for role
    const [termsAccepted, setTermsAccepted] = useState(false);
    const [message, setMessage] = useState('');  // New state for success/error message

    const handleSignup = async (e) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            setMessage("Passwords do not match!");
            return;
        }

        const data = {
            name,
            phone_number: phone,
            email,
            password,
            address,
            user_type: customerType,
            role  // Include role in the data
        };

        try {
            const response = await fetch('http://localhost:8000/api/v1/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Signup failed');
            }

            const result = await response.json();
            setMessage(result.message);  // Set success message
            alert(result.message);  // Display success message in a popup

            // Reset form fields
            setName('');
            setPhone('');
            setEmail('');
            setPassword('');
            setConfirmPassword('');
            setAddress('');
            setCustomerType('individual');
            setRole('customer');  // Reset role
            setTermsAccepted(false);
        } catch (error) {
            setMessage(error.message);  // Set error message
            alert(error.message);  // Display error message in a popup
        }
    };

    const handleForgotPassword = () => {
        console.log('Forgot Password for:', email);
    };

    return (
        <div className="signup-component" style={{ maxWidth: '600px', margin: '0 auto', padding: '20px', border: '1px solid #ccc', borderRadius: '10px' }}>
            <h2>Sign Up</h2>
            {message && <p>{message}</p>}  // Display message
            <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <input
                    type="text"
                    placeholder="Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />
                <input
                    type="tel"
                    placeholder="Phone Number"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    required
                />
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                />
                <textarea
                    placeholder="Regular Address"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    required
                />
                <select
                    value={customerType}
                    onChange={(e) => setCustomerType(e.target.value)}
                >
                    <option value="individual">Individual</option>
                    <option value="enterprise">Enterprise</option>
                </select>
                <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                >
                    <option value="customer">Customer</option>
                    <option value="legal_counsel">Legal Counsel</option>
                    <option value="arbitrator">Arbitrator</option>
                </select>
                <div className="captcha-placeholder">Captcha Placeholder</div>
                <div style={{ maxHeight: '100px', overflowY: 'scroll', border: '1px solid #ccc', padding: '5px', marginBottom: '10px' }}>
                    <p>This is terms and condition for now</p>
                </div>
                <div>
                    <input
                        type="checkbox"
                        checked={termsAccepted}
                        onChange={(e) => setTermsAccepted(e.target.checked)}
                        required
                    />
                    <label>I accept the <a href="#">terms and conditions</a></label>
                </div>
                <button type="submit">Sign Up</button>
            </form>
            <button onClick={handleForgotPassword}>Forgot Password?</button>
        </div>
    );
};

export default SignupComponent; 