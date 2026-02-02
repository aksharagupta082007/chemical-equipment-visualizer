import React from 'react';

const EquipmentTable = ({ dataset }) => {
  if (!dataset || !dataset.equipment_type_distribution) return null;

  const rows = Object.entries(dataset.equipment_type_distribution);

  return (
    <table border="1">
      <thead>
        <tr>
          <th>Equipment Type</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(([type, count]) => (
          <tr key={type}>
            <td>{type}</td>
            <td>{count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default EquipmentTable;
