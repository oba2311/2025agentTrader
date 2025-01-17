import React, { useState } from "react";

interface SignUpFormProps {
	onSubmit: (data: {
		email: string;
		password: string;
		confirmPassword: string;
	}) => void;
}

const SignUpForm: React.FC<SignUpFormProps> = ({ onSubmit }) => {
	const [formData, setFormData] = useState({
		email: "",
		password: "",
		confirmPassword: "",
	});

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		onSubmit(formData);
	};

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { name, value } = e.target;
		setFormData((prev) => ({
			...prev,
			[name]: value,
		}));
	};

	return (
		<form onSubmit={handleSubmit} className="signup-form">
			<div className="form-group">
				<label htmlFor="email">Email:</label>
				<input
					type="email"
					id="email"
					name="email"
					value={formData.email}
					onChange={handleChange}
					required
				/>
			</div>

			<div className="form-group">
				<label htmlFor="password">Password:</label>
				<input
					type="password"
					id="password"
					name="password"
					value={formData.password}
					onChange={handleChange}
					required
				/>
			</div>

			<div className="form-group">
				<label htmlFor="confirmPassword">Confirm Password:</label>
				<input
					type="password"
					id="confirmPassword"
					name="confirmPassword"
					value={formData.confirmPassword}
					onChange={handleChange}
					required
				/>
			</div>

			<button type="submit">Sign Up</button>
		</form>
	);
};

export default SignUpForm;
