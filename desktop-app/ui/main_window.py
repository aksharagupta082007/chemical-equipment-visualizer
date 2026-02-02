import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem,
    QHBoxLayout, QFrame, QScrollArea, QSplitter, QInputDialog, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from ui.charts import ChartsCanvas

# Updated Import to use the Class
from services.api_client import ChemicalAPIClient

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize the API client
        self.api = ChemicalAPIClient()
        
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(50, 50, 1600, 950)
        self.dataset = None
        self.history = []
        
        self.apply_theme()
        self.initUI()
        
        # Authentication Trigger
        if self.handle_login():
            self.load_history()
        else:
            QMessageBox.critical(self, "Access Denied", "Valid login required to use this application.")
            sys.exit()

    def handle_login(self):
        """Simple popup to handle JWT Authentication"""
        user, ok1 = QInputDialog.getText(self, "Login", "Username:", QLineEdit.Normal)
        if not ok1: return False
        
        pw, ok2 = QInputDialog.getText(self, "Login", "Password:", QLineEdit.Password)
        if not ok2: return False
        
        return self.api.login(user, pw)

    def apply_theme(self):
        """Apply chemical engineering neon theme"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0a0e27, stop:0.5 #1a1f3a, stop:1 #0a0e27);
                color: #e0e6ed;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 229, 255, 0.3), stop:1 rgba(0, 229, 255, 0.1));
                border: 2px solid #00e5ff;
                border-radius: 8px;
                padding: 10px 20px;
                color: #00e5ff;
                font-weight: bold;
                font-size: 13px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 229, 255, 0.5), stop:1 rgba(0, 229, 255, 0.2));
                border: 3px solid #00e5ff;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 229, 255, 0.7), stop:1 rgba(0, 229, 255, 0.4));
                border: 3px solid #7c4dff;
            }
            
            QLabel {
                color: #e0e6ed;
                padding: 4px;
                font-size: 12px;
            }
            
            QLabel#titleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #00e5ff;
                padding: 12px;
                background: rgba(10, 14, 39, 0.8);
                border-radius: 10px;
                border: 2px solid #00e5ff;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            
            QLabel#subtitleLabel {
                font-size: 12px;
                color: #7c4dff;
                padding: 6px;
                font-weight: 600;
                letter-spacing: 1px;
            }
            
            QLabel#statusLabel {
                background: rgba(26, 31, 58, 0.8);
                border-radius: 6px;
                border-left: 4px solid #00e5ff;
                padding: 10px;
                font-size: 12px;
                color: #00e5ff;
                font-weight: 500;
            }
            
            QLabel#sectionLabel {
                font-size: 13px;
                font-weight: bold;
                color: #00e5ff;
                padding: 8px 6px;
                margin-top: 4px;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                border-bottom: 2px solid #00e5ff;
            }
            
            QTableWidget {
                background: rgba(10, 14, 39, 0.7);
                border: 2px solid rgba(0, 229, 255, 0.3);
                border-radius: 8px;
                gridline-color: rgba(124, 77, 255, 0.2);
                color: #e0e6ed;
                padding: 6px;
                selection-background-color: rgba(0, 229, 255, 0.3);
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid rgba(124, 77, 255, 0.15);
            }
            
            QTableWidget::item:selected {
                background: rgba(0, 229, 255, 0.25);
                color: #ffffff;
                border: 1px solid #00e5ff;
            }
            
            QTableWidget::item:hover {
                background: rgba(124, 77, 255, 0.15);
            }
            
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 229, 255, 0.3), stop:1 rgba(26, 31, 58, 0.8));
                color: #00e5ff;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #00e5ff;
                font-weight: bold;
                font-size: 12px;
                text-transform: uppercase;
            }
            
            QListWidget {
                background: rgba(10, 14, 39, 0.7);
                border: 2px solid rgba(124, 77, 255, 0.3);
                border-radius: 8px;
                padding: 6px;
                color: #e0e6ed;
            }
            
            QListWidget::item {
                padding: 8px;
                border-radius: 6px;
                margin: 2px 0px;
                background: rgba(26, 35, 50, 0.5);
                border-left: 3px solid transparent;
                color: #e0e6ed;
            }
            
            QListWidget::item:hover {
                background: rgba(0, 229, 255, 0.15);
                border-left: 3px solid #00e5ff;
            }
            
            QListWidget::item:selected {
                background: rgba(124, 77, 255, 0.3);
                border-left: 3px solid #7c4dff;
                color: #ffffff;
            }
            
            QScrollBar:vertical {
                background: rgba(10, 14, 39, 0.6);
                width: 14px;
                border-radius: 7px;
                margin: 0px;
                border: 1px solid rgba(0, 229, 255, 0.2);
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00e5ff, stop:1 #7c4dff);
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c4dff, stop:1 #00e5ff);
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background: rgba(10, 14, 39, 0.6);
                height: 14px;
                border-radius: 7px;
                margin: 0px;
                border: 1px solid rgba(0, 229, 255, 0.2);
            }
            
            QScrollBar::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00e5ff, stop:1 #7c4dff);
                border-radius: 6px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7c4dff, stop:1 #00e5ff);
            }
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            
            QFrame#glassPanel {
                background: rgba(10, 14, 39, 0.7);
                border: 2px solid rgba(0, 229, 255, 0.25);
                border-radius: 10px;
                padding: 12px;
            }
            
            QFrame#glowPanel {
                background: rgba(10, 14, 39, 0.8);
                border: 2px solid rgba(124, 77, 255, 0.4);
                border-radius: 10px;
                padding: 12px;
            }
            
            QSplitter::handle {
                background: rgba(0, 229, 255, 0.2);
                width: 2px;
            }
            
            QSplitter::handle:hover {
                background: rgba(0, 229, 255, 0.5);
            }
        """)

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        # HEADER
        title = QLabel("CHEMICAL EQUIPMENT VISUALIZER")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(55)
        main_layout.addWidget(title)

        subtitle = QLabel("Desktop Application | Parameter Analysis & Visualization")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        # UPLOAD SECTION
        uploadFrame = QFrame()
        uploadFrame.setObjectName("glassPanel")
        uploadLayout = QVBoxLayout()
        uploadLayout.setContentsMargins(8, 6, 8, 6)
        uploadLayout.setSpacing(6)
        
        self.uploadBtn = QPushButton("UPLOAD CSV DATASET")
        self.uploadBtn.clicked.connect(self.upload_file)
        self.uploadBtn.setMaximumHeight(45)
        uploadLayout.addWidget(self.uploadBtn)

        self.statusLabel = QLabel("Ready to analyze | Upload CSV file with equipment data")
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setAlignment(Qt.AlignCenter)
        uploadLayout.addWidget(self.statusLabel)
        
        uploadFrame.setLayout(uploadLayout)
        main_layout.addWidget(uploadFrame)

        # TABLE AND HISTORY
        contentSplitter = QSplitter(Qt.Horizontal)
        
        leftFrame = QFrame()
        leftFrame.setObjectName("glassPanel")
        leftLayout = QVBoxLayout()
        leftLayout.setContentsMargins(6, 4, 6, 4)
        leftLayout.setSpacing(4)
        
        summaryLabel = QLabel("SUMMARY STATISTICS")
        summaryLabel.setObjectName("sectionLabel")
        leftLayout.addWidget(summaryLabel)
        
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(False)
        self.table.setShowGrid(True)
        self.table.setMaximumHeight(140)
        leftLayout.addWidget(self.table)
        
        leftFrame.setLayout(leftLayout)
        contentSplitter.addWidget(leftFrame)

        rightFrame = QFrame()
        rightFrame.setObjectName("glassPanel")
        rightLayout = QVBoxLayout()
        rightLayout.setContentsMargins(6, 4, 6, 4)
        rightLayout.setSpacing(4)
        
        timelineLabel = QLabel("UPLOAD HISTORY")
        timelineLabel.setObjectName("sectionLabel")
        rightLayout.addWidget(timelineLabel)
        
        self.timeline = QListWidget()
        self.timeline.setMaximumHeight(140)
        rightLayout.addWidget(self.timeline)
        
        rightFrame.setLayout(rightLayout)
        contentSplitter.addWidget(rightFrame)
        
        contentSplitter.setSizes([600, 400])
        contentSplitter.setChildrenCollapsible(False)
        
        main_layout.addWidget(contentSplitter)

        # CHARTS
        self.chartFrame = QFrame()
        self.chartFrame.setObjectName("glowPanel")
        self.chartLayout = QVBoxLayout()
        self.chartLayout.setContentsMargins(8, 6, 8, 8)
        self.chartLayout.setSpacing(4)
        
        chartLabel = QLabel("VISUALIZATIONS & ANALYTICS")
        chartLabel.setObjectName("sectionLabel")
        self.chartLayout.addWidget(chartLabel)
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        self.chartContainer = QWidget()
        self.chartContainerLayout = QVBoxLayout()
        self.chartContainerLayout.setContentsMargins(0, 0, 0, 0)
        self.chartContainer.setLayout(self.chartContainerLayout)
        
        self.scrollArea.setWidget(self.chartContainer)
        self.chartLayout.addWidget(self.scrollArea)
        
        self.canvas = None
        self.chartFrame.setLayout(self.chartLayout)
        
        main_layout.addWidget(self.chartFrame, stretch=10) 

        # FOOTER
        footer = QLabel("Chemical Engineering Analytics | Real-time Parameter Monitoring | Django + React + PyQt5")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            color: #7c4dff;
            font-size: 9px;
            padding: 4px;
            margin-top: 2px;
            font-weight: 500;
            letter-spacing: 0.5px;
        """)
        main_layout.addWidget(footer)

        self.setLayout(main_layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV Dataset", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                # Updated to use self.api
                self.dataset = self.api.upload_csv(file_path)
                filename = file_path.split('/')[-1]
                
                total_eq = self.dataset.get('total_equipment', 0)
                self.statusLabel.setText(f"SUCCESS | Dataset '{filename}' uploaded | {total_eq} entries processed")
                self.statusLabel.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(0, 197, 131, 0.3), stop:1 rgba(0, 229, 255, 0.2));
                    border-radius: 6px;
                    border-left: 4px solid #00c853;
                    padding: 10px;
                    font-size: 12px;
                    color: #00e5ff;
                    font-weight: 600;
                """)
                
                self.show_summary()
                self.show_charts()
                self.load_history()
                
            except Exception as e:
                self.statusLabel.setText(f"ERROR | Upload failed: {str(e)}")
                self.statusLabel.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgba(255, 82, 82, 0.3), stop:1 rgba(255, 64, 129, 0.2));
                    border-radius: 6px;
                    border-left: 4px solid #ff5252;
                    padding: 10px;
                    font-size: 12px;
                    color: #ff4081;
                    font-weight: 600;
                """)

    def show_summary(self):
        if not self.dataset:
            return
        
        summary_keys = ["total_equipment", "avg_flowrate", "avg_pressure", "avg_temperature"]
        self.table.setRowCount(len(summary_keys))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["PARAMETER", "VALUE"])
        
        labels = {"total_equipment": "[EQUIP]", "avg_flowrate": "[FLOW]", "avg_pressure": "[PRESS]", "avg_temperature": "[TEMP]"}
        units = {"total_equipment": "units", "avg_flowrate": "L/min", "avg_pressure": "atm", "avg_temperature": "K"}
        
        for i, key in enumerate(summary_keys):
            metric_name = key.replace("_", " ").upper()
            label, unit = labels.get(key, "[DATA]"), units.get(key, "")
            value = self.dataset.get(key, 0)
            
            param_item = QTableWidgetItem(f"{label} {metric_name}")
            param_item.setFont(QFont("Segoe UI", 10, QFont.Bold))
            
            val_str = f"{int(value)} {unit}" if key == "total_equipment" else f"{value:.2f} {unit}"
            value_item = QTableWidgetItem(val_str)
            value_item.setFont(QFont("Segoe UI", 10))
            value_item.setForeground(QColor("#00e5ff"))
            
            self.table.setItem(i, 0, param_item)
            self.table.setItem(i, 1, value_item)
        
        self.table.resizeColumnsToContents()

    def show_charts(self):
        if self.canvas:
            self.chartContainerLayout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        
        self.canvas = ChartsCanvas(self.dataset)
        self.chartContainerLayout.addWidget(self.canvas)

    def load_history(self):
        try:
            # Updated to use self.api
            self.history = self.api.fetch_history()
            self.timeline.clear()
            
            if not self.history:
                placeholder = QListWidgetItem("[EMPTY] No upload history available yet")
                placeholder.setForeground(QColor("#7c4dff"))
                self.timeline.addItem(placeholder)
            else:
                for d in self.history:
                    timestamp = d.get('uploaded_at', 'Unknown time')
                    filename = d.get('filename', 'Unknown file')
                    
                    item = QListWidgetItem(f"[FILE] {filename}")
                    item.setFont(QFont("Segoe UI", 9))
                    self.timeline.addItem(item)
                    
                    time_item = QListWidgetItem(f"      [TIME] {timestamp}")
                    time_item.setForeground(QColor("#7c4dff"))
                    time_item.setFont(QFont("Segoe UI", 8))
                    self.timeline.addItem(time_item)
                    
        except Exception as e:
            error_item = QListWidgetItem(f"[ERROR] Unable to fetch history: {str(e)}")
            error_item.setForeground(QColor("#ff5252"))
            self.timeline.addItem(error_item)

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()