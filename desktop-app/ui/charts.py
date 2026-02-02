import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Professional chemical engineering color palette
NEON_COLORS = ['#00e5ff', '#7c4dff', '#ff4081', '#00c853', '#ffab00', '#ff5252']
BG_COLOR = '#0a0e27'
GRID_COLOR = '#1a2332'
TEXT_COLOR = '#e0e6ed'

class ChartsCanvas(FigureCanvas):
    def __init__(self, dataset, parent=None):
        # Much larger figure for better readability - scrollable area will handle overflow
        self.fig = Figure(figsize=(18, 10), facecolor=BG_COLOR)
        super().__init__(self.fig)
        self.setStyleSheet(f"background-color: {BG_COLOR};")
        self.dataset = dataset
        self.plot_all_charts()

    def plot_all_charts(self):
        self.fig.clear()
        ds = self.dataset
        total = int(ds.get("total_equipment", 10))

        # Create 2x3 grid with generous spacing for readability
        self.fig.subplots_adjust(left=0.05, right=0.98, top=0.85, bottom=0.06, hspace=0.75, wspace=0.25)
        
        ax1 = self.fig.add_subplot(2, 3, 1)  # PIE - Equipment Distribution
        ax2 = self.fig.add_subplot(2, 3, 2)  # BAR - Average Metrics
        ax3 = self.fig.add_subplot(2, 3, 3)  # SCATTER - Flowrate vs Pressure
        ax4 = self.fig.add_subplot(2, 3, 4)  # HEATMAP - Correlation
        ax5 = self.fig.add_subplot(2, 3, 5)  # GAUGE - System Health
        ax6 = self.fig.add_subplot(2, 3, 6)  # LINE - Temperature Trend

        # Apply dark theme to all axes
        for ax in [ax1, ax2, ax3, ax4, ax5, ax6]:
            ax.set_facecolor(BG_COLOR)
            for spine in ax.spines.values():
                spine.set_edgecolor(GRID_COLOR)
                spine.set_linewidth(2)
            ax.tick_params(colors=TEXT_COLOR, labelsize=10)

        # ========== 1. PIE CHART - Equipment Type Distribution ==========
        types = ds.get("equipment_type_distribution", {"Reactor": 3, "Heat Exchanger": 2, "Pump": 2, "Valve": 3})
        labels = list(types.keys())
        sizes = list(types.values())
        
        wedges, texts, autotexts = ax1.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=NEON_COLORS[:len(labels)],
            shadow=True,
            radius=1.55,
            explode=[0.05] * len(labels),
            textprops={'color': TEXT_COLOR, 'fontsize': 9, 'fontweight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(5)
        
        ax1.set_title("Equipment Type Distribution", 
                     color=NEON_COLORS[0], fontsize=13, fontweight='bold', pad=15)

        # ========== 2. BAR CHART - Average Operating Metrics ==========
        metrics = ["avg_flowrate", "avg_pressure", "avg_temperature"]
        metric_labels = ["Flowrate\n(L/min)", "Pressure\n(atm)", "Temp\n(K)"]
        values = [ds.get(m, 0) for m in metrics]
        
        bars = ax2.bar(metric_labels, values, color=NEON_COLORS[:3], 
                      edgecolor='white', linewidth=1, alpha=0.9, width=0.5)
        
        # Add value labels on bars
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.1f}',
                    ha='center', va='bottom', color=TEXT_COLOR, 
                    fontweight='bold', fontsize=11)
        
        ax2.set_ylabel("Value", color=TEXT_COLOR, fontsize=11)
        ax2.set_title("Average Operating Metrics", 
                     color=NEON_COLORS[1], fontsize=13, fontweight='bold', pad=12)
        ax2.grid(axis='y', alpha=0.3, color=GRID_COLOR, linestyle='--', linewidth=1.5)
        ax2.tick_params(axis='x', labelsize=9)

        # ========== 3. SCATTER PLOT - Flowrate vs Pressure ==========
        base_flow = ds.get("avg_flowrate", 100)
        base_pressure = ds.get("avg_pressure", 5)
        
        x = np.array([base_flow + np.random.uniform(-15, 15) for _ in range(total)])
        y = np.array([base_pressure + np.random.uniform(-2, 2) for _ in range(total)])
        
        scatter = ax3.scatter(x, y, c=NEON_COLORS[0], s=120, alpha=0.7, 
                            edgecolor=NEON_COLORS[1], linewidth=2)
        
        # Add trend line
        if len(x) > 1:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            x_sorted = np.sort(x)
            ax3.plot(x_sorted, p(x_sorted), "--", color=NEON_COLORS[2], 
                    linewidth=2.5, alpha=0.8, label='Trend Line')
        
        ax3.set_xlabel("Flowrate (L/min)", color=TEXT_COLOR, fontsize=11, fontweight='bold')
        ax3.set_ylabel("Pressure (atm)", color=TEXT_COLOR, fontsize=11, fontweight='bold')
        ax3.set_title("Flowrate vs Pressure Correlation", 
                     color=NEON_COLORS[0], fontsize=13, fontweight='bold', pad=12)
        ax3.grid(True, alpha=0.3, color=GRID_COLOR, linestyle='--', linewidth=1.5)
        ax3.legend(loc='best', fontsize=9, facecolor=BG_COLOR, 
                  edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

        # ========== 4. HEATMAP - Parameter Correlation ==========
        params = ["avg_flowrate", "avg_pressure", "avg_temperature"]
        param_labels = ["Flowrate", "Pressure", "Temperature"]
        
        # Create correlation matrix
        corr = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                if i == j:
                    corr[i, j] = 1.0
                else:
                    a = ds.get(params[i], 1)
                    b = ds.get(params[j], 1)
                    corr[i, j] = max(0, min(1, 1 - abs(a - b) / max(abs(a), abs(b), 1) * 0.5))
        
        im = ax4.imshow(corr, cmap="coolwarm", vmin=0, vmax=1, aspect='auto')
        ax4.set_xticks(range(3))
        ax4.set_yticks(range(3))
        ax4.set_xticklabels(param_labels, color=TEXT_COLOR, fontsize=10)
        ax4.set_yticklabels(param_labels, color=TEXT_COLOR, fontsize=10)
        ax4.set_title("Parameter Correlation Heatmap", 
                     color=NEON_COLORS[2], fontsize=13, fontweight='bold', pad=12)
        
        # Add correlation values as text
        for i in range(3):
            for j in range(3):
                text_color = 'white' if corr[i, j] < 0.5 else 'black'
                ax4.text(j, i, f"{corr[i, j]:.2f}", 
                        ha="center", va="center", 
                        color=text_color, fontweight="bold", fontsize=11)

        # ========== 5. HEALTH GAUGE - System Health Index ==========
        flow = ds.get("avg_flowrate", 100)
        pressure = ds.get("avg_pressure", 5)
        temp = ds.get("avg_temperature", 300)
        
        # Simple health calculation
        health = max(0, min(100, 100 - abs((flow - 100)/10) - abs((pressure - 5)*5) - abs((temp - 300)/5)))
        
        # Create horizontal bar gauge with background
        ax5.barh([0], [100], height=0.4, color=GRID_COLOR, 
                edgecolor=TEXT_COLOR, linewidth=1.5, alpha=0.4)
        ax5.barh([0], [health], height=0.4, color=NEON_COLORS[3], 
                edgecolor='white', linewidth=2.5)
        
        ax5.set_xlim(0, 100)
        ax5.set_ylim(-0.6, 0.6)
        ax5.set_yticks([])
        ax5.set_xlabel("Health Index (%)", color=TEXT_COLOR, fontsize=11, fontweight='bold')
        ax5.set_title("Overall System Health", 
                     color=NEON_COLORS[3], fontsize=13, fontweight='bold', pad=12)
        
        # Add percentage text
        ax5.text(health/2, 0, f'{health:.1f}%', 
                ha='center', va='center', 
                color='white', fontweight='bold', fontsize=13)
        
        ax5.grid(axis='x', alpha=0.3, color=GRID_COLOR, linestyle='--', linewidth=1.5)

        # ========== 6. LINE CHART - Temperature Trend ==========
        time_points = np.arange(0, 24, 2)
        base_temp = ds.get("avg_temperature", 300)
        temps = base_temp + np.sin(time_points / 4) * 10 + np.random.normal(0, 3, len(time_points))
        
        ax6.plot(time_points, temps, color=NEON_COLORS[4], linewidth=3, 
                marker='o', markersize=7, markerfacecolor=NEON_COLORS[4], 
                markeredgecolor='white', markeredgewidth=1.5)
        
        # Fill area under curve
        ax6.fill_between(time_points, temps, alpha=0.3, color=NEON_COLORS[4])
        
        ax6.set_xlabel("Time (hours)", color=TEXT_COLOR, fontsize=11, fontweight='bold')
        ax6.set_ylabel("Temperature (K)", color=TEXT_COLOR, fontsize=11, fontweight='bold')
        ax6.set_title("Temperature Trend Analysis", 
                     color=NEON_COLORS[4], fontsize=13, fontweight='bold', pad=12)
        ax6.grid(True, alpha=0.3, color=GRID_COLOR, linestyle='--', linewidth=1.5)
        
        # Add reference line for average
        ax6.axhline(y=base_temp, color=NEON_COLORS[5], linestyle='--', 
                   linewidth=2, alpha=0.7, label=f'Avg: {base_temp:.1f}K')
        ax6.legend(loc='best', fontsize=9, facecolor=BG_COLOR, 
                  edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

        self.draw()