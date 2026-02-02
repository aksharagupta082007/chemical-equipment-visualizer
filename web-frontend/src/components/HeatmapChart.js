import React, { useMemo } from "react";

const parameters = ["Flowrate", "Pressure", "Temperature"];

// Correlation calculation
const getCorrelation = (a, b) => {
  if (a === b) return 1;
  return Math.max(0, Math.min(1, 1 - Math.abs(a - b) / Math.max(a, b)));
};

// Color scale (dark → neon)
const getColor = (value) => `rgba(0, 229, 255, ${0.2 + 0.8 * value})`;

const HeatmapChart = ({ dataset }) => {
  if (!dataset) return null;

  const values = {
    Flowrate: dataset.avg_flowrate,
    Pressure: dataset.avg_pressure,
    Temperature: dataset.avg_temperature,
  };

  const heatmapData = useMemo(() => {
    return parameters.map((row) =>
      parameters.map((col) => ({
        row,
        col,
        value: getCorrelation(values[row], values[col]),
      }))
    );
  }, [dataset]);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `80px repeat(${parameters.length}, 1fr)`,
        gap: "10px",
        color: "#ccc",
        fontSize: "14px",
        padding: "10px",
      }}
    >
      {/* Header Row */}
      <div />
      {parameters.map((p) => (
        <div
          key={p}
          style={{
            textAlign: "center",
            color: "#00e5ff",
            fontWeight: 600,
          }}
        >
          {p}
        </div>
      ))}

      {/* Heatmap Rows */}
      {heatmapData.map((rowData, i) => (
        <React.Fragment key={i}>
          <div
            style={{
              color: "#00e5ff",
              fontWeight: 600,
              display: "flex",
              alignItems: "center",
            }}
          >
            {parameters[i]}
          </div>

          {rowData.map((cell, j) => {
            const intensity = cell.value;
            return (
              <div
                key={j}
                title={`${cell.row} ↔ ${cell.col}: ${intensity.toFixed(2)}`}
                style={{
                  height: "42px",
                  borderRadius: "6px",
                  background: getColor(intensity),
                  boxShadow: `0 0 ${intensity * 18}px rgba(0,229,255,${0.7 +
                    0.3 * intensity})`,
                  transition: "transform 0.3s ease, box-shadow 0.3s ease, opacity 0.5s ease",
                  opacity: 0,
                  animation: `fadeIn 0.5s forwards ${0.05 * (i * parameters.length + j)}s`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#00e5ff",
                  fontWeight: 600,
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "scale(1.1)";
                  e.currentTarget.style.boxShadow = `0 0 ${intensity *
                    30}px rgba(0,255,255,1)`;
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "scale(1)";
                  e.currentTarget.style.boxShadow = `0 0 ${intensity *
                    18}px rgba(0,229,255,${0.7 + 0.3 * intensity})`;
                }}
              >
                {intensity.toFixed(2)}
              </div>
            );
          })}
        </React.Fragment>
      ))}

      {/* Fade-in Animation */}
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
        `}
      </style>
    </div>
  );
};

export default HeatmapChart;
