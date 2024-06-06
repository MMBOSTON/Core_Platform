import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';

const CustomerNPSChart = ({ data }) => {
    const [chartData, setChartData] = useState({});

    useEffect(() => {
        if (data.length > 0) {
            const customerNames = data.map(item => item.name);
            const npsScores = data.map(item => item.nps_score);

            setChartData({
                labels: customerNames,
                datasets: [
                    {
                        label: 'NPS Score',
                        data: npsScores,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }
                ]
            });
        }
    }, [data]);

    return (
        <div className="customer-nps-chart">
            <h2>Customer NPS Scores</h2>
            {chartData.labels && chartData.labels.length > 0 ? (
                <Line data={chartData} />
            ) : (
                <p>Loading chart...</p>
            )}
        </div>
    );
};

export default CustomerNPSChart;

