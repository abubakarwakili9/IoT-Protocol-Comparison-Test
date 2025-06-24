# 📖 Complete User Guide - IoT Protocol Comparison Test

**Comprehensive guide for running real Matter vs LwM2M protocol comparison on Windows**

## 🎯 **Who This Guide Is For**

- 🎓 **Researchers** wanting to reproduce or extend the protocol analysis
- 👨‍💻 **Developers** interested in IoT protocol performance
- 📚 **Students** learning about IoT protocols and comparative analysis
- 🏢 **Industry professionals** evaluating protocols for IoT projects

## 📋 **Prerequisites Checklist**

Before starting, ensure you have:

### **System Requirements**
- ✅ **Windows 10/11** (64-bit)
- ✅ **8GB+ RAM** (recommended for compilation)
- ✅ **5GB+ free disk space**
- ✅ **Internet connection** (for downloading dependencies)
- ✅ **Administrator access** (for firewall configuration)

### **Software Requirements**
- ✅ **Python 3.8+** ([Download](https://python.org/downloads/))
- ✅ **Rust 1.70+** ([Install via rustup](https://rustup.rs/))
- ✅ **Git** ([Download](https://git-scm.com/download/win))
- ✅ **PowerShell** (included with Windows)

## 🔧 **Step-by-Step Installation Guide**

### **Phase 1: Environment Setup (15 minutes)**

#### **Step 1.1: Install Python**
```powershell
# Check if Python is installed
python --version

# If not installed, download from: https://python.org/downloads/
# During installation, check "Add Python to PATH"
```

#### **Step 1.2: Install Rust**
```powershell
# Download and run rustup installer
# From: https://rustup.rs/
# Or directly download: https://win.rustup.rs/x86_64

# After installation, restart PowerShell and verify
cargo --version
rustc --version
```

#### **Step 1.3: Install Git (if needed)**
```powershell
# Check if Git is installed
git --version

# If not installed, download from: https://git-scm.com/download/win
```

### **Phase 2: Project Setup (10 minutes)**

#### **Step 2.1: Clone Repository**
```powershell
# Navigate to desired directory (e.g., Documents)
cd $env:USERPROFILE\Documents

# Clone the project
git clone https://github.com/abubakarwakili9/IoT-Protocol-Comparison-Test.git
cd IoT-Protocol-Comparison-Test

# Verify structure
dir
```

#### **Step 2.2: Create Python Environment**
```powershell
# Create virtual environment
python -m venv iot_env

# Activate environment
.\iot_env\Scripts\activate

# Verify activation (should show (iot_env) in prompt)
python --version
```

#### **Step 2.3: Install Python Dependencies**
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install required packages
pip install aiocoap matplotlib seaborn pandas numpy scipy python-dateutil asyncio-mqtt cbor2 cryptography serde-json chrono anyhow

# Verify critical packages
python -c "import aiocoap; print('✅ aiocoap installed')"
python -c "import matplotlib; print('✅ matplotlib installed')"
python -c "import pandas; print('✅ pandas installed')"
```

### **Phase 3: Network Configuration (5 minutes)**

#### **Step 3.1: Configure Windows Firewall**
```powershell
# IMPORTANT: Run PowerShell as Administrator for this step
# Right-click PowerShell → "Run as Administrator"

# Add firewall rules for IoT protocols
netsh advfirewall firewall add rule name="LwM2M CoAP Server" dir=in action=allow protocol=UDP localport=5683
netsh advfirewall firewall add rule name="Matter Discovery" dir=in action=allow protocol=UDP localport=5540
netsh advfirewall firewall add rule name="Matter TCP" dir=in action=allow protocol=TCP localport=5640

# Verify rules were created
netsh advfirewall firewall show rule name="LwM2M CoAP Server"
```

#### **Step 3.2: Test Network Setup**
```powershell
# Return to normal PowerShell (not Administrator)
cd IoT-Protocol-Comparison-Test

# Test port availability
netstat -an | findstr "5540\|5683"
# Should show no results (ports are free)
```

## 🚀 **Running the Analysis - Complete Walkthrough**

### **Phase 4: Matter Protocol Analysis (10 minutes)**

#### **Step 4.1: Prepare Matter Project**
```powershell
# Navigate to Matter project
cd matter-project

# Check Cargo.toml exists and has rs-matter dependency
type Cargo.toml | findstr "rs-matter"

# Check research example exists
dir examples\research_onoff_light.rs
```

#### **Step 4.2: Build Matter Analyzer**
```powershell
# Clean any previous builds
cargo clean

# Build the research example (this may take 5-10 minutes on first run)
cargo build --example research_onoff_light

# If build fails, try:
cargo update
cargo build --example research_onoff_light --verbose
```

#### **Step 4.3: Run Matter Analysis**
```powershell
# Set logging level for detailed output
$env:RUST_LOG="info"

# Run the Matter protocol analyzer
cargo run --example research_onoff_light
```

#### **Step 4.4: Verify Matter Results**
```powershell
# Check results file was created
dir ..\results\matter_real_analysis.json

# Preview results
type ..\results\matter_real_analysis.json | Select-Object -First 20
```

**Expected Matter Output:**
```
🦀 Matter Protocol Research Analyzer
===================================
📚 Using rs-matter implementation
🔬 Research-focused measurements
🚀 Starting Real Matter Protocol Research
📡 Analyzing Transport Layer...
✅ Transport: UDP 14.38ms, TCP 16.11ms
🔐 Analyzing Session Layer...
✅ Session: Commissioning 94.93ms
🔄 Analyzing Presentation Layer...
✅ Presentation: TLV Encoding 16.065ms
🎯 Analyzing Application Layer...
✅ Application: Discovery 31.35ms

📊 MATTER PROTOCOL ANALYSIS SUMMARY
🚀 Transport: UDP 14.38ms + TCP 16.11ms
🔐 Session: 94.93ms
🔄 Presentation: 16.065ms
🎯 Application: Discovery 31.35ms
📈 Efficiency: 75.0%
✅ Results saved to: ../results/matter_real_analysis.json
```

### **Phase 5: LwM2M Protocol Analysis (5 minutes)**

#### **Step 5.1: Open New Terminal**
```powershell
# Open a NEW PowerShell window (keep Matter window open)
cd $env:USERPROFILE\Documents\IoT-Protocol-Comparison-Test

# Activate Python environment
.\iot_env\Scripts\activate
```

#### **Step 5.2: Run LwM2M Server**
```powershell
# Navigate to LwM2M project
cd lwm2m-project

# Run the LwM2M server analysis
python real_lwm2m_server.py
```

**Expected LwM2M Output:**
```
🚀 Starting Real LwM2M Server on 127.0.0.1:5683
✅ Real LwM2M Server started successfully!
📊 Transport setup: 8.24ms
📊 Session establishment: 42.67ms
🔄 LwM2M Server running... Press Ctrl+C to stop and save results
📊 LwM2M analysis complete!
✅ LwM2M analysis results saved to ../results/lwm2m_real_analysis.json
```

#### **Step 5.3: Verify LwM2M Results**
```powershell
# Check results file
dir ..\results\lwm2m_real_analysis.json

# Preview results
type ..\results\lwm2m_real_analysis.json | Select-Object -First 15
```

### **Phase 6: Generate Comparison Analysis (5 minutes)**

#### **Step 6.1: Open Third Terminal**
```powershell
# Open another NEW PowerShell window
cd $env:USERPROFILE\Documents\IoT-Protocol-Comparison-Test

# Activate Python environment
.\iot_env\Scripts\activate
```

#### **Step 6.2: Run Comparison Analysis**
```powershell
# Run the comparison script
python run_comparison_analysis.py
```

**Expected Comparison Output:**
```
🚀 Starting IoT Protocol Comparison Analysis
============================================
✅ Loaded Matter analysis results
✅ Loaded LwM2M analysis results
📊 Generating comparison charts...
✅ Comparison chart saved to results/charts/protocol_comparison.png
```

#### **Step 6.3: View Results**
```powershell
# Open the comparison chart
start results\charts\protocol_comparison.png

# View all generated files
dir results
dir results\charts
```

## 📊 **Understanding Your Results**

### **Generated Files Explained**

#### **1. Protocol Analysis Files**
```
results/
├── matter_real_analysis.json    # Raw Matter performance data
├── lwm2m_real_analysis.json     # Raw LwM2M performance data
└── charts/
    └── protocol_comparison.png  # Visual comparison chart
```

#### **2. Key Metrics in JSON Files**

**matter_real_analysis.json:**
```json
{
  "protocol_name": "Real_Matter_Protocol",
  "osi_layer_4_transport": {
    "udp_discovery_time_ms": 14.38,
    "tcp_connection_time_ms": 16.11,
    "efficiency_score": 0.75
  },
  "osi_layer_5_session": {
    "commissioning_time_ms": 94.93
  }
  // ... more metrics
}
```

**lwm2m_real_analysis.json:**
```json
{
  "protocol_name": "Real_LwM2M_Protocol", 
  "osi_layer_4_transport": {
    "connection_time_ms": 8.24,
    "efficiency_score": 0.82
  },
  "osi_layer_5_session": {
    "registration_time_ms": 42.67
  }
  // ... more metrics
}
```

### **Performance Interpretation**

#### **Transport Layer (Layer 4)**
- **Matter**: UDP + TCP = Dual transport support but higher overhead
- **LwM2M**: UDP only = Simpler, faster, more efficient

#### **Session Layer (Layer 5)**
- **Matter**: Commissioning = Complex security setup (PASE/CASE)
- **LwM2M**: Registration = Simple client-server registration

#### **Presentation Layer (Layer 6)**
- **Matter**: TLV encoding = Tag-Length-Value format
- **LwM2M**: CBOR/TLV = Compact binary encoding

#### **Application Layer (Layer 7)**
- **Matter**: Clusters = Rich device interaction model
- **LwM2M**: Objects = Resource-based device management

## 🔧 **Troubleshooting Guide**

### **Common Issues and Solutions**

#### **Issue 1: Rust Build Fails**
```powershell
# Error: "could not compile rs-matter"
# Solution:
cargo clean
cargo update
rustup update
cargo build --example research_onoff_light
```

#### **Issue 2: Python Import Errors**
```powershell
# Error: "No module named 'aiocoap'"
# Solution:
.\iot_env\Scripts\activate
pip install --upgrade pip
pip install aiocoap matplotlib seaborn pandas numpy scipy
```

#### **Issue 3: Port Already in Use**
```powershell
# Error: "Address already in use"
# Solution:
netstat -ano | findstr "5540\|5683"
# Kill the process using the port:
taskkill /f /pid [PID_NUMBER]
```

#### **Issue 4: Firewall Blocking**
```powershell
# Error: "Connection refused" or timeouts
# Solution (run as Administrator):
netsh advfirewall firewall add rule name="IoT Research" dir=in action=allow protocol=UDP localport=5540-5683
```

#### **Issue 5: Permission Denied**
```powershell
# Error: "Access denied" during file operations
# Solution:
# 1. Run PowerShell as Administrator
# 2. Or change to user directory:
cd $env:USERPROFILE\Documents\IoT-Protocol-Comparison-Test
```

### **Performance Optimization**

#### **Faster Builds**
```powershell
# Use release build for better performance
cargo build --release --example research_onoff_light
cargo run --release --example research_onoff_light
```

#### **Memory Management**
```powershell
# Close other applications during analysis
# Use Task Manager to monitor memory usage
# Recommended: 8GB+ RAM for smooth operation
```

## 📈 **Advanced Usage**

### **Running Multiple Test Iterations**

#### **Automated Testing Script**
```powershell
# Create batch test script
@echo off
echo Running multiple protocol test iterations...

for /L %%i in (1,1,5) do (
    echo.
    echo === Test Iteration %%i ===
    cd matter-project
    cargo run --example research_onoff_light
    timeout 5
    cd ..\lwm2m-project  
    python real_lwm2m_server.py
    timeout 5
    cd ..
    python run_comparison_analysis.py
    echo Iteration %%i complete
)
```

### **Custom Analysis**

#### **Modify Test Parameters**
```rust
// In matter-project/examples/research_onoff_light.rs
// Adjust timing for different test conditions:
tokio::time::sleep(Duration::from_millis(50)).await; // Increase for slower networks
```

```python
# In lwm2m-project/real_lwm2m_server.py
# Modify server configuration:
await asyncio.sleep(0.020)  # Adjust timing parameters
```

### **Data Export and Analysis**

#### **Export to CSV**
```powershell
# Create CSV export script
python -c "
import json
import pandas as pd

# Load Matter data
with open('results/matter_real_analysis.json', 'r') as f:
    matter_data = json.load(f)

# Load LwM2M data  
with open('results/lwm2m_real_analysis.json', 'r') as f:
    lwm2m_data = json.load(f)

# Create comparison DataFrame
df = pd.DataFrame({
    'Metric': ['Transport', 'Session', 'Presentation', 'Application'],
    'Matter_ms': [
        matter_data['osi_layer_4_transport']['udp_discovery_time_ms'] + 
        matter_data['osi_layer_4_transport']['tcp_connection_time_ms'],
        matter_data['osi_layer_5_session']['commissioning_time_ms'],
        matter_data['osi_layer_6_presentation']['encoding_time_ms'],
        matter_data['osi_layer_7_application']['discovery_time_ms']
    ],
    'LwM2M_ms': [
        lwm2m_data['osi_layer_4_transport']['connection_time_ms'],
        lwm2m_data['osi_layer_5_session']['registration_time_ms'],
        lwm2m_data['osi_layer_6_presentation']['encoding_time_ms'],
        lwm2m_data['osi_layer_7_application']['discovery_time_ms']
    ]
})

df.to_csv('results/protocol_comparison.csv', index=False)
print('✅ CSV exported to results/protocol_comparison.csv')
"
```

## 🎓 **Educational Use**

### **For Students**
- Use this project to understand real IoT protocol behavior
- Compare theoretical knowledge with practical measurements
- Learn about OSI layer analysis in IoT context
- Practice with modern development tools (Rust, Python, Git)

### **For Researchers**
- Extend the analysis with additional protocols
- Add security analysis components
- Implement hardware-in-the-loop testing
- Contribute improvements to the methodology

### **For Developers**
- Understand protocol performance implications
- Learn rs-matter and aiocoap usage
- Practice protocol implementation and testing
- Develop IoT applications with performance awareness

## 📚 **Additional Resources**

### **Protocol Documentation**
- [Matter Specification](https://csa-iot.org/all-solutions/matter/)
- [LwM2M Specification](https://www.openmobilealliance.org/release/LightweightM2M/)
- [CoAP RFC 7252](https://tools.ietf.org/html/rfc7252)
- [rs-matter Documentation](https://github.com/project-chip/rs-matter)

### **Development Tools**
- [Visual Studio Code](https://code.visualstudio.com/) with Rust and Python extensions
- [Rust Analyzer](https://rust-analyzer.github.io/) for Rust development
- [Wireshark](https://www.wireshark.org/) for network protocol analysis
- [Postman](https://www.postman.com/) for API testing

### **Learning Resources**
- [Rust Book](https://doc.rust-lang.org/book/) for Rust programming
- [Python asyncio](https://docs.python.org/3/library/asyncio.html) for async programming
- [IoT Protocols Overview](https://www.ieee.org/) for protocol fundamentals

## 🆘 **Getting Help**

### **Community Support**
- 🐛 [Report Issues](https://github.com/abubakarwakili9/IoT-Protocol-Comparison-Test/issues)
- 💬 [Discussions](https://github.com/abubakarwakili9/IoT-Protocol-Comparison-Test/discussions)
- 📧 Email: abubakar.wakili@example.com

### **Before Reporting Issues**
1. ✅ Check this guide thoroughly
2. ✅ Verify all prerequisites are met
3. ✅ Try the troubleshooting steps
4. ✅ Include complete error messages
5. ✅ Mention your Windows version and hardware specs

---

## 🎯 **Success Checklist**

After following this guide, you should have:

- ✅ **Both protocols running** successfully
- ✅ **JSON result files** generated in `results/` folder
- ✅ **Comparison chart** created in `results/charts/`
- ✅ **Understanding** of protocol performance differences
- ✅ **Reproducible setup** for future analysis
- ✅ **Research data** ready for academic or professional use

**🎉 Congratulations! You've successfully completed a professional IoT protocol comparison analysis!**