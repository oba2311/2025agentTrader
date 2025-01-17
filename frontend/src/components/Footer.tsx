const Footer = () => {
	return (
		<footer className="fixed bottom-0 left-0 right-0 bg-gray-50 py-4 text-center text-sm text-gray-600 shadow-md">
			<p className="mb-2">
				Built with <span className="text-blue-500">💙</span> by OBA and the open
				source community
			</p>
			<a
				href="https://github.com/oba2311/trader-agent"
				target="_blank"
				rel="noopener noreferrer"
				className="text-blue-500 hover:text-blue-600 underline"
			>
				View on GitHub
			</a>
		</footer>
	);
};

export default Footer;
