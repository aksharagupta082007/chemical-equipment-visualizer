import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import UploadCSV from "./components/UploadCSV";
import { SummaryCards, Timeline } from "./components/SummaryCards";
import EquipmentTable from "./components/EquipmentTable";
import Charts from "./components/Charts";
import { getHistory } from "./services/api";

// ---------------- Dashboard Component ----------------
const Dashboard = ({ latestDataset, history, error, isLoading }) => {
  
  // --- PDF Download Function ---
  const handleDownloadPDF = async () => {
    const reportElement = document.getElementById("report-content");
    const downloadBtn = document.getElementById("download-btn-container");

    // Temporarily hide the download button so it doesn't appear in the PDF
    if (downloadBtn) downloadBtn.style.visibility = "hidden";

    try {
      const canvas = await html2canvas(reportElement, {
        scale: 2, // High resolution
        useCORS: true,
        backgroundColor: "#0a0a20", // Match your theme background
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");
      
      const imgProps = pdf.getImageProperties(imgData);
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

      pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
      pdf.save(`Chemical_Equipment_Report_${new Date().toLocaleDateString()}.pdf`);
    } catch (err) {
      console.error("PDF Generation failed:", err);
      alert("Failed to generate PDF. Please try again.");
    } finally {
      // Show the button again
      if (downloadBtn) downloadBtn.style.visibility = "visible";
    }
  };

  if (isLoading) {
    return (
      <div style={{ textAlign: "center", marginTop: "100px" }}>
        <div className="spinner" style={{ marginBottom: "20px", fontSize: "2rem" }}>🌀</div>
        <p style={{ color: "#00e5ff", letterSpacing: "3px", fontWeight: "bold" }}>
          RESTORING SESSION...
        </p>
      </div>
    );
  }

  if (!latestDataset && !error) return <Navigate to="/" />;

  return (
    <div className="dashboard-content animate-fade-in" style={{ paddingBottom: "40px" }}>
      
      {/* Download Button Section */}
      <div id="download-btn-container" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '20px' }}>
        <button 
          onClick={handleDownloadPDF}
          style={{ 
            background: 'rgba(0, 229, 255, 0.1)', 
            border: '1px solid #00e5ff', 
            color: '#00e5ff', 
            padding: '10px 20px', 
            cursor: 'pointer', 
            fontFamily: 'Orbitron',
            boxShadow: '0 0 10px rgba(0, 229, 255, 0.2)'
          }}
        >
          📥 EXPORT PDF REPORT
        </button>
      </div>

      {/* --- This ID wraps everything to be included in the PDF --- */}
      <div id="report-content" style={{ padding: '10px' }}>
        <h2 style={{ marginBottom: "20px", textShadow: "0 0 5px #00e5ff" }}>📊 Latest Dataset Summary</h2>
        
        <div className="card" style={{ backdropFilter: "blur(12px)", background: "rgba(20,20,40,0.6)", marginBottom: "20px" }}>
          <SummaryCards dataset={latestDataset} />
        </div>

        <div className="card" style={{ backdropFilter: "blur(12px)", background: "rgba(20,20,40,0.6)", marginBottom: "20px" }}>
          <Charts dataset={latestDataset} />
        </div>

        <div className="card" style={{ backdropFilter: "blur(12px)", background: "rgba(20,20,40,0.6)", marginBottom: "20px" }}>
          <EquipmentTable dataset={latestDataset} />
        </div>

        <h2 style={{ marginTop: "40px", marginBottom: "20px", textShadow: "0 0 5px #00e5ff" }}>🕒 Upload Timeline</h2>
        <div className="card" style={{ backdropFilter: "blur(12px)", background: "rgba(20,20,40,0.6)" }}>
          <Timeline history={history} />
        </div>
      </div>
      {/* --- End of PDF Wrap --- */}
    
      <div style={{ textAlign: 'center', marginTop: '40px' }}>
        <button 
          onClick={() => window.location.href = "/"}
          style={{ background: 'transparent', border: '1px solid #00e5ff', color: '#00e5ff', padding: '10px 20px', cursor: 'pointer', fontFamily: 'Orbitron' }}
        >
          RETURN TO PORTAL
        </button>
      </div>
    </div>
  );
};

// ---------------- Main App ----------------
function App() {
  const [latestDataset, setLatestDataset] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [jwtToken, setJwtToken] = useState(localStorage.getItem("accessToken") || "");

  const fetchHistory = async () => {
    if (!jwtToken) return; 
    setIsLoading(true);
    try {
      const response = await getHistory(jwtToken); 
      const data = response.data || [];
      setHistory(data);
      if (data.length > 0) setLatestDataset(data[0]);
      setError(null);
    } catch (err) {
      console.error("Backend error:", err);
      if (err.response?.status === 401) {
        setError("Session expired or invalid. Please set a new token.");
      } else {
        setError("Backend Connection Error");
      }
      setLatestDataset(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (jwtToken) {
      fetchHistory();
    }
  }, [jwtToken]);

  // ---------- Neon Grid Background Logic ----------
  useEffect(() => {
    const canvas = document.getElementById("neonGrid");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);
    const gridSize = 40;
    const speed = 0.2;
    let offset = 0;

    const draw = () => {
      ctx.clearRect(0, 0, w, h);
      ctx.strokeStyle = "rgba(0,229,255,0.08)";
      ctx.lineWidth = 1;
      for (let x = 0; x < w; x += gridSize) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
      }
      for (let y = 0; y < h; y += gridSize) {
        ctx.beginPath(); ctx.moveTo(0, y + offset); ctx.lineTo(w, y + offset); ctx.stroke();
      }
      offset += speed;
      if (offset > gridSize) offset = 0;
      requestAnimationFrame(draw);
    };
    draw();
    const handleResize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <Router>
      <div style={{ position: "relative", minHeight: "100vh", fontFamily: "Orbitron, sans-serif", color: "#00e5ff" }}>
        <canvas id="neonGrid" style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", zIndex: -1 }} />

        <div style={{ padding: "20px", maxWidth: "1200px", margin: "0 auto" }}>
          <h1 style={{ textAlign: "center", marginBottom: "40px", textShadow: "0 0 15px #00e5ff", fontSize: '2.5rem' }}>
            ⚗️ Chemical Equipment Visualizer
          </h1>

          {error && (
            <div className="card" style={{ borderColor: "#fb7185", background: "rgba(40,20,20,0.6)", marginBottom: "20px", padding: '15px' }}>
              <p style={{ color: "#fb7185", textAlign: 'center', margin: 0 }}>{error}</p>
            </div>
          )}

          <Routes>
            <Route path="/" element={
              <div style={{ display: 'flex', justifyContent: 'center', marginTop: '50px' }}>
                <div className="card" style={{ 
                  backdropFilter: "blur(12px)", 
                  background: "rgba(20,20,40,0.7)", 
                  textAlign: 'center', 
                  padding: '60px',
                  border: '1px solid #00e5ff',
                  boxShadow: '0 0 20px rgba(0, 229, 255, 0.2)',
                  maxWidth: '600px',
                  width: '100%'
                }}>
                  <h2 style={{ color: '#00e5ff', marginBottom: '30px', letterSpacing: '2px' }}>SYSTEM PORTAL</h2>

                  <UploadCSV 
                    token={jwtToken} 
                    onUploadSuccess={() => fetchHistory()} 
                  />

                  <div style={{ marginTop: '30px' }}>
                    <button 
                      style={{ background: '#00e5ff', color: '#0a0a20', border: 'none', padding: '10px 20px', cursor: 'pointer', fontFamily: 'Orbitron', fontWeight: 'bold', borderRadius: '4px', marginRight: '10px' }}
                      onClick={() => {
                        const token = prompt("Paste your JWT access token here:");
                        if (token) {
                          setJwtToken(token);
                          localStorage.setItem("accessToken", token);
                        }
                      }}
                    >
                      {jwtToken ? "Update Token" : "Set JWT Token"}
                    </button>

                    {jwtToken && (
                        <button 
                            style={{ background: 'transparent', color: '#fb7185', border: '1px solid #fb7185', padding: '10px 20px', cursor: 'pointer', fontFamily: 'Orbitron', borderRadius: '4px' }}
                            onClick={() => {
                                localStorage.removeItem("accessToken");
                                setJwtToken("");
                                setHistory([]);
                                setLatestDataset(null);
                            }}
                        >
                            Logout
                        </button>
                    )}
                  </div>
                </div>
              </div>
            } />

            <Route path="/dashboard" element={
              <Dashboard 
                latestDataset={latestDataset} 
                history={history} 
                error={error} 
                isLoading={isLoading}
              />
            } />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;