import React from "react";

/* ============================
   🧠 SUMMARY CARDS
============================ */
const SummaryCards = ({ dataset }) => {
  if (!dataset) return null;

  const cardStyle = {
    background: "rgba(15,20,40,0.65)",
    backdropFilter: "blur(12px)",
    borderRadius: "14px",
    padding: "16px 18px",
    minWidth: "160px",
    boxShadow: "0 0 25px rgba(0,229,255,0.18)",
  };

  const labelStyle = {
    color: "#94a3b8",
    fontSize: "12px",
    marginBottom: "6px",
  };

  const valueStyle = {
    color: "#00e5ff",
    fontSize: "20px",
    fontWeight: 600,
    textShadow: "0 0 10px rgba(0,229,255,0.6)",
  };

  return (
    <div style={{ display: "flex", gap: "18px", flexWrap: "wrap" }}>
      <div style={cardStyle}>
        <div style={labelStyle}>Total Equipment</div>
        <div style={valueStyle}>{dataset.total_equipment}</div>
      </div>

      <div style={cardStyle}>
        <div style={labelStyle}>Avg Flowrate (bar)</div>
        <div style={valueStyle}>{dataset.avg_flowrate.toFixed(2)}</div>
      </div>

      <div style={cardStyle}>
        <div style={labelStyle}>Avg Pressure (psi)</div>
        <div style={valueStyle}>{dataset.avg_pressure.toFixed(2)}</div>
      </div>

      <div style={cardStyle}>
        <div style={labelStyle}>Avg Temperature (°C)</div>
        <div style={valueStyle}>{dataset.avg_temperature.toFixed(2)}</div>
      </div>
    </div>
  );
};

/* ============================
   🕒 GLOWING TIMELINE
============================ */
const Timeline = ({ history }) => {
  if (!history || history.length === 0)
    return <p style={{ color: "#94a3b8" }}>No uploads yet.</p>;

  return (
    <div style={{ position: "relative", marginLeft: "18px", marginTop: "20px" }}>
      {/* Vertical neon line */}
      <div
        style={{
          position: "absolute",
          left: "12px",
          top: 0,
          bottom: 0,
          width: "4px",
          background: "linear-gradient(to bottom, #00e5ff, #7c4dff)",
          borderRadius: "2px",
          opacity: 0.35,
        }}
      />

      <ul style={{ listStyle: "none", padding: 0 }}>
        {history.map((item) => (
          <li
            key={item.id}
            style={{
              marginBottom: "22px",
              position: "relative",
              paddingLeft: "34px",
            }}
          >
            {/* Glowing node */}
            <span
              style={{
                position: "absolute",
                left: "0px",
                top: "2px",
                width: "20px",
                height: "20px",
                borderRadius: "50%",
                background: "linear-gradient(45deg, #00e5ff, #7c4dff)",
                boxShadow:
                  "0 0 12px #00e5ff, 0 0 24px rgba(124,77,255,0.8)",
              }}
            />

            <div style={{ color: "#e5e7eb", fontSize: "14px" }}>
              {item.filename}
              <br />
              <span style={{ color: "#00e5ff", fontSize: "12px" }}>
                {new Date(item.uploaded_at).toLocaleString()}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

/* ============================
   EXPORTS
============================ */
export { SummaryCards, Timeline };
