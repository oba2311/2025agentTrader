import { FaGithub } from "react-icons/fa";

const Contributors = () => {
	return (
		<div className="flex flex-col items-center justify-center">
			<h2 className="text-2xl font-bold text-center mb-4 md:mb-8">
				Magnificent Contributors:
				<br />
				<span className="text-sm text-gray-500">your name here!</span>
			</h2>
			<FaGithub />
		</div>
	);
};

export default Contributors;
