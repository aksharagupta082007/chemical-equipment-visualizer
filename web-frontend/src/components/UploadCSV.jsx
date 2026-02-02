import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const UploadCSV = ({ onUploadSuccess, token }) => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a CSV file");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`, // 🔥 send JWT token
          },
        }
      );

      // Call parent callback to update dashboard
      if (onUploadSuccess) onUploadSuccess(response.data);

      // Optional: navigate to dashboard after upload
      navigate("/dashboard");
    } catch (error) {
      console.error("Upload failed:", error);
      alert(
        error.response?.data?.error || "Upload failed! Check console for details."
      );
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "20px",
      }}
    >
      <p style={{ color: "#94a3b8" }}>
        Initialize system by uploading telemetry data (.csv)
      </p>

      <div
        style={{
          border: "2px dashed #00e5ff",
          padding: "20px",
          borderRadius: "8px",
          background: "rgba(0, 229, 255, 0.05)",
        }}
      >
        <input
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          style={{ color: "#00e5ff", cursor: "pointer" }}
        />
      </div>

      <button
        onClick={handleUpload}
        style={{
          background: "#00e5ff",
          color: "#0a0a20",
          border: "none",
          padding: "12px 30px",
          fontFamily: "Orbitron",
          fontWeight: "bold",
          borderRadius: "4px",
          cursor: "pointer",
          boxShadow: "0 0 15px #00e5ff",
          transition: "all 0.3s",
        }}
        onMouseOver={(e) => (e.target.style.boxShadow = "0 0 25px #00e5ff")}
        onMouseOut={(e) => (e.target.style.boxShadow = "0 0 15px #00e5ff")}
      >
        UPLOAD CSV & LAUNCH
      </button>
    </div>
  );
};

export default UploadCSV;
