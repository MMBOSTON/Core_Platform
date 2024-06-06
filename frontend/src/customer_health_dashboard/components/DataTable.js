import React from 'react';
import './DataTable.css'; // Assuming you have a CSS file for styling

const DataTable = ({ data }) => {
  return (
    <table>
      <thead>
        <tr>
          <th>Customer ID</th>
          <th>Usage Frequency</th>
          <th>Support Tickets</th>
          <th>NPS Score</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.customerId}>
            <td>{item.customerId}</td>
            <td>{item.usageFrequency}</td>
            <td>{item.supportTickets}</td>
            <td>{item.npsScore}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default DataTable;