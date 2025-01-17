import { useEffect, useState } from "react";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	Legend,
	ResponsiveContainer,
} from "recharts";
import { StockData, processStockData } from "../utils/dataProcessor";

const StockChart = () => {
	const [data, setData] = useState<StockData[]>([]);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const processedData = await processStockData();
				setData(processedData);
			} catch (error) {
				console.error("Error fetching stock data:", error);
			}
		};

		fetchData();
	}, []);

	const formatQuarter = (dateStr: string) => {
		const date = new Date(dateStr);
		const quarter = Math.floor(date.getMonth() / 3) + 1;
		return `Q${quarter} ${date.getFullYear()}`;
	};

	const isQuarterStart = (dateStr: string) => {
		const date = new Date(dateStr);
		return date.getMonth() % 3 === 0;
	};

	const renderLabel = (props: any) => {
		const { x, y, stroke } = props;
		if (x === undefined || y === undefined) return null;
		if (props.index !== data.length - 1) return null;

		return (
			<text
				x={x}
				y={y}
				dx={10}
				dy={3}
				fill={stroke}
				fontSize={12}
				textAnchor="start"
			>
				{props.name}
			</text>
		);
	};

	return (
		<div className="w-full h-[50vh] md:h-[70vh] lg:h-[80vh]">
			<h2 className="text-xl md:text-2xl font-bold text-center mb-4 md:mb-8">
				20-Day Rolling Average Performance (% Change)
			</h2>
			<h3 className="text-sm text-center italic mb-4 md:mb-8">
				Tap to see detailed view 👇🏻
			</h3>
			<div className="h-[calc(100%-8rem)]">
				<ResponsiveContainer>
					<LineChart
						data={data}
						margin={{ right: 16, left: -0, top: 5, bottom: 10 }}
					>
						<CartesianGrid strokeDasharray="3 3" />
						<XAxis
							dataKey="date"
							tickFormatter={formatQuarter}
							ticks={data
								.filter((d) => isQuarterStart(d.date))
								.map((d) => d.date)}
							tick={{ fontSize: 12 }}
						/>
						<YAxis
							tick={{ fontSize: 12 }}
							tickFormatter={(value) => `${value}%`}
							width={35}
						/>
						<Tooltip
							labelFormatter={(date) => new Date(date).toLocaleDateString()}
							formatter={(value: number) => [value.toFixed(2) + "%"]}
						/>
						<Legend
							wrapperStyle={{
								fontSize: "12px",
								marginTop: "20px",
								paddingBottom: "40px",
							}}
						/>
						<Line
							type="monotone"
							dataKey="SPY"
							stroke="#8884d8"
							name="S&P 500"
							dot={false}
							strokeWidth={2}
							label={renderLabel}
						/>
						<Line
							type="monotone"
							dataKey="SMH"
							stroke="#82ca9d"
							name="Semicon ETF"
							dot={false}
							label={renderLabel}
						/>
						<Line
							type="monotone"
							dataKey="NVDA"
							stroke="#ff7300"
							name="NVIDIA"
							dot={false}
							label={renderLabel}
						/>
						<Line
							type="monotone"
							dataKey="AMD"
							stroke="#ff0000"
							name="AMD"
							dot={false}
							label={renderLabel}
						/>
					</LineChart>
				</ResponsiveContainer>
			</div>
		</div>
	);
};

export default StockChart;
