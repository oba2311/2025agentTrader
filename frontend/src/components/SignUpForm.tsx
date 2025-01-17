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
		<div className="w-full max-w-sm md:max-w-lg mx-auto px-4 md:px-6">
			<form
				onSubmit={handleSubmit}
				className="bg-white rounded-lg shadow-xl p-6 md:p-8 space-y-4 md:space-y-6"
			>
				<h2 className="text-xl md:text-2xl font-bold text-gray-800 mb-6 md:mb-8 text-center">
					Get notified when your target price is met!
				</h2>

				<div className="space-y-2">
					<label
						htmlFor="email"
						className="block text-sm font-medium text-gray-700"
					>
						Email
					</label>
					<input
						type="email"
						id="email"
						name="email"
						value={formData.email}
						onChange={handleChange}
						required
						className="w-full px-3 md:px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
						placeholder="you@example.com"
					/>
				</div>

				<button
					type="submit"
					className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-2 px-4 rounded-md hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 font-medium text-sm md:text-base"
				>
					Sign Up
				</button>
			</form>
		</div>
	);
};

export default SignUpForm;
