import React, { useState, useMemo } from "react";
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  CartesianGrid,
  Sector,
} from "recharts";

import HeatmapChart from "./HeatmapChart";

/* ---------- COLORS ---------- */
const COLORS = [
  "#00e5ff",
  "#7c4dff",
  "#ff4081",
  "#00c853",
  "#ffab00",
  "#ff5252",
];

/* ---------- GLASS CARD ---------- */
const GlassCard = ({ title, children }) => (
  <div
    style={{
      background: "rgba(15,20,40,0.65)",
      backdropFilter: "blur(14px)",
      borderRadius: "18px",
      padding: "20px",
      boxShadow: "0 0 35px rgba(0,255,255,0.18)",
    }}
  >
    <h3 style={{ color: "#00e5ff", marginBottom: "14px" }}>{title}</h3>
    {children}
  </div>
);

/* ---------- NEON TOOLTIP (FIXES BLACK TEXT) ---------- */
const NeonTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;

  return (
    <div
      style={{
        background: "rgba(10,15,30,0.96)",
        border: "1px solid #00e5ff",
        borderRadius: "10px",
        padding: "10px 14px",
        boxShadow: "0 0 18px rgba(0,229,255,0.7)",
      }}
    >
      {label && (
        <p style={{ margin: 0, color: "#7c4dff", fontWeight: 600 }}>
          {label}
        </p>
      )}

      {payload.map((entry, i) => (
        <p
          key={i}
          style={{
            margin: "6px 0 0",
            color: entry.color || "#00e5ff",
            fontWeight: 600,
          }}
        >
          {entry.name}:{" "}
          <span style={{ color: "#00e5ff", fontWeight: 700 }}>
            {entry.value}
          </span>
        </p>
      ))}
    </div>
  );
};

/* ---------- 3D PIE SLICE ---------- */
const ActivePieSlice = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  startAngle,
  endAngle,
  fill,
}) => {
  const RADIAN = Math.PI / 180;
  const sin = Math.sin(-RADIAN * midAngle);
  const cos = Math.cos(-RADIAN * midAngle);

  return (
    <Sector
      cx={cx + cos * 10}
      cy={cy + sin * 10}
      innerRadius={innerRadius}
      outerRadius={outerRadius + 12}
      startAngle={startAngle}
      endAngle={endAngle}
      fill={fill}
      style={{
        filter: "drop-shadow(0 0 14px rgba(0,229,255,0.9))",
      }}
    />
  );
};

/* ---------- NEON BAR (NO WHITE FLASH) ---------- */
const ActiveBar = ({ x, y, width, height }) => (
  <g>
    <defs>
      <linearGradient id="barGlow" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#00e5ff" />
        <stop offset="100%" stopColor="#7c4dff" />
      </linearGradient>
    </defs>

    <rect
      x={x - 4}
      y={y - 6}
      width={width + 8}
      height={height + 8}
      rx={12}
      fill="url(#barGlow)"
      style={{
        filter: "drop-shadow(0 0 14px rgba(0,229,255,0.9))",
      }}
    />
  </g>
);

function Charts({ dataset }) {
  if (!dataset) return null;

  const pieData = Object.entries(
    dataset.equipment_type_distribution || {}
  ).map(([name, value]) => ({ name, value }));

  const avgBarData = [
    { name: "Flowrate", value: dataset.avg_flowrate },
    { name: "Pressure", value: dataset.avg_pressure },
    { name: "Temperature", value: dataset.avg_temperature },
  ];

  const scatterData = useMemo(
    () =>
      Array.from({ length: dataset.total_equipment }).map(() => ({
        x: dataset.avg_flowrate + Math.random() * 30 - 15,
        y: dataset.avg_pressure + Math.random() * 4 - 2,
      })),
    [dataset]
  );

  const [activeIndex, setActiveIndex] = useState(null);

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
        gap: "26px",
        marginTop: "30px",
      }}
    >
      {/* PIE */}
      <GlassCard title="Equipment Type Distribution">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={pieData}
              dataKey="value"
              innerRadius={60}
              outerRadius={95}
              activeIndex={activeIndex}
              activeShape={ActivePieSlice}
              onMouseEnter={(_, i) => setActiveIndex(i)}
              onMouseLeave={() => setActiveIndex(null)}
            >
              {pieData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<NeonTooltip />} cursor={{ fill: "transparent" }} />
          </PieChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* BAR */}
      <GlassCard title="Average Operating Metrics">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={avgBarData}>
            <CartesianGrid stroke="rgba(255,255,255,0.07)" />
            <XAxis dataKey="name" stroke="#aaa" />
            <YAxis stroke="#aaa" />
            <Tooltip content={<NeonTooltip />} cursor={{ fill: "transparent" }} />
            <Bar dataKey="value" activeBar={<ActiveBar />}>
              {avgBarData.map((_, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* SCATTER */}
      <GlassCard title="Flowrate vs Pressure">
        <ResponsiveContainer width="100%" height={280}>
          <ScatterChart>
            <CartesianGrid stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="x" stroke="#aaa" />
            <YAxis dataKey="y" stroke="#aaa" />
            <Tooltip content={<NeonTooltip />} />
            <Scatter data={scatterData} fill="#00e5ff" />
          </ScatterChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* VERTICAL BAR */}
      <GlassCard title="Equipment Count by Type">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart layout="vertical" data={pieData}>
            <CartesianGrid stroke="rgba(255,255,255,0.05)" />
            <XAxis type="number" stroke="#aaa" />
            <YAxis dataKey="name" type="category" stroke="#aaa" />
            <Tooltip content={<NeonTooltip />} />
            <Bar dataKey="value" activeBar={<ActiveBar />}>
              {pieData.map((_, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </GlassCard>

      {/* HEATMAP */}
      <GlassCard title="Parameter Correlation Heatmap">
        <HeatmapChart dataset={dataset} />
      </GlassCard>

      {/* HEALTH */}
      <GlassCard title="Overall System Health">
        <h1
          style={{
            color: "#00e5ff",
            textAlign: "center",
            fontSize: "56px",
            textShadow: "0 0 18px rgba(0,229,255,0.8)",
          }}
        >
          {Math.max(
            0,
            Math.round(
              100 -
                (dataset.avg_flowrate +
                  dataset.avg_pressure +
                  dataset.avg_temperature) /
                  10
            )
          )}
          %
        </h1>
      </GlassCard>
    </div>
  );
}

export default Charts;
