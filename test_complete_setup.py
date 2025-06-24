import subprocess
import sys
import os
import time

def test_python_environment():
    """Test Python environment"""
    print("🐍 Testing Python Environment...")
    
    required_packages = ['aiocoap', 'matplotlib', 'seaborn', 'pandas', 'numpy', 'scipy']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - Missing")
            return False
    return True

def test_rust_environment():
    """Test Rust environment"""
    print("\n🦀 Testing Rust Environment...")
    
    try:
        result = subprocess.run(['cargo', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Cargo - {result.stdout.strip()}")
            return True
        else:
            print("❌ Cargo - Not found")
            return False
    except:
        print("❌ Cargo - Not found")
        return False

def test_firewall_ports():
    """Test if firewall ports are accessible"""
    print("\n🔥 Testing Firewall Configuration...")
    
    import socket
    
    ports = [
        (5683, "UDP", "LwM2M/CoAP"),
        (5540, "UDP", "Matter Discovery"), 
        (5640, "TCP", "Matter TCP")
    ]
    
    success = True
    for port, protocol, description in ports:
        try:
            if protocol == "UDP":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            sock.bind(('127.0.0.1', port))
            sock.close()
            print(f"✅ {description} ({protocol} {port}) - OK")
        except Exception as e:
            print(f"❌ {description} ({protocol} {port}) - Error: {e}")
            success = False
    
    return success

def main():
    print("🧪 IoT Protocol Comparison - Complete Setup Test")
    print("=" * 55)
    
    python_ok = test_python_environment()
    rust_ok = test_rust_environment()
    firewall_ok = test_firewall_ports()
    
    print(f"\n📋 SETUP TEST RESULTS")
    print("-" * 25)
    print(f"Python Environment: {'✅ PASS' if python_ok else '❌ FAIL'}")
    print(f"Rust Environment:   {'✅ PASS' if rust_ok else '❌ FAIL'}")
    print(f"Firewall Config:    {'✅ PASS' if firewall_ok else '❌ FAIL'}")
    
    if python_ok and rust_ok and firewall_ok:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"🚀 Your environment is ready for IoT protocol testing!")
        print(f"\nNext steps:")
        print(f"1. cd matter-project && cargo run")
        print(f"2. cd lwm2m-project && python real_lwm2m_server.py")
        print(f"3. python run_comparison_analysis.py")
    else:
        print(f"\n⚠️ Some tests failed. Please fix the issues above.")
        
        if not python_ok:
            print(f"   Fix: pip install aiocoap matplotlib seaborn pandas numpy scipy")
        if not rust_ok:
            print(f"   Fix: Install Rust from https://rustup.rs/")
        if not firewall_ok:
            print(f"   Fix: Run firewall setup as Administrator")

if __name__ == "__main__":
    main()