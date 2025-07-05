"""
Real LwM2M Objects Implementation (OMA Standard)
"""
import time
import random

class LwM2MObject:
    """Base class for all LwM2M objects"""
    def __init__(self, object_id):
        self.object_id = object_id
        self.instances = {}
    
    def create_instance(self, instance_id):
        self.instances[instance_id] = {}
        return True
    
    def delete_instance(self, instance_id):
        if instance_id in self.instances:
            del self.instances[instance_id]
            return True
        return False

class SecurityObject(LwM2MObject):
    """Object 0: LwM2M Security"""
    def __init__(self):
        super().__init__(0)
        self.create_instance(0)  # Bootstrap server
        self.create_instance(1)  # LwM2M server
        
    def get_server_uri(self, instance_id):
        """Resource 0: Server URI"""
        if instance_id == 0:
            return "coap://bootstrap.example.com:5683"
        return "coap://127.0.0.1:5683"
    
    def get_is_bootstrap(self, instance_id):
        """Resource 1: Bootstrap Server"""
        return instance_id == 0
    
    def get_security_mode(self, instance_id):
        """Resource 2: Security Mode (0=PSK, 1=RPK, 2=Certificate, 3=NoSec)"""
        return 3  # NoSec for testing
    
    def get_public_key_identity(self, instance_id):
        """Resource 3: Public Key or Identity"""
        return "test_identity"
    
    def get_server_public_key(self, instance_id):
        """Resource 4: Server Public Key"""
        return "test_server_key"

class ServerObject(LwM2MObject):
    """Object 1: LwM2M Server"""
    def __init__(self):
        super().__init__(1)
        self.create_instance(0)
        
    def get_server_id(self, instance_id):
        """Resource 0: Short Server ID"""
        return 1
    
    def get_lifetime(self, instance_id):
        """Resource 1: Lifetime"""
        return 86400  # 24 hours
    
    def get_default_min_period(self, instance_id):
        """Resource 2: Default Minimum Period"""
        return 10
    
    def get_default_max_period(self, instance_id):
        """Resource 3: Default Maximum Period"""
        return 3600
    
    def get_notification_storing(self, instance_id):
        """Resource 6: Notification Storing When Disabled or Offline"""
        return False
    
    def get_binding(self, instance_id):
        """Resource 7: Binding (U=UDP, T=TCP, S=SMS)"""
        return "U"

class DeviceObject(LwM2MObject):
    """Object 3: Device"""
    def __init__(self):
        super().__init__(3)
        self.create_instance(0)
        
    def get_manufacturer(self, instance_id):
        """Resource 0: Manufacturer"""
        return "IoT Research Lab"
    
    def get_model_number(self, instance_id):
        """Resource 1: Model Number"""
        return "LwM2M-Test-Device-v1.0"
    
    def get_serial_number(self, instance_id):
        """Resource 2: Serial Number"""
        return f"SN{random.randint(100000, 999999)}"
    
    def get_firmware_version(self, instance_id):
        """Resource 3: Firmware Version"""
        return "1.0.0"
    
    def get_available_power_sources(self, instance_id):
        """Resource 6: Available Power Sources"""
        return [1, 5]  # 1=DC power, 5=USB
    
    def get_power_source_voltage(self, instance_id):
        """Resource 7: Power Source Voltage"""
        return [5000, 5000]  # 5V in mV
    
    def get_battery_level(self, instance_id):
        """Resource 9: Battery Level (0-100)"""
        return random.randint(20, 100)
    
    def get_memory_free(self, instance_id):
        """Resource 10: Memory Free (KB)"""
        return random.randint(50, 200)
    
    def get_error_code(self, instance_id):
        """Resource 11: Error Code"""
        return [0]  # No error
    
    def execute_reboot(self, instance_id):
        """Resource 4: Reboot (Executable)"""
        print(f"🔄 Device {instance_id} rebooting...")
        return True
    
    def get_current_time(self, instance_id):
        """Resource 13: Current Time"""
        return int(time.time())
    
    def get_utc_offset(self, instance_id):
        """Resource 14: UTC Offset"""
        return "+00:00"
    
    def get_timezone(self, instance_id):
        """Resource 15: Timezone"""
        return "UTC"

class ConnectivityMonitoringObject(LwM2MObject):
    """Object 4: Connectivity Monitoring"""
    def __init__(self):
        super().__init__(4)
        self.create_instance(0)
        
    def get_network_bearer(self, instance_id):
        """Resource 0: Network Bearer"""
        return 21  # WLAN
    
    def get_available_network_bearer(self, instance_id):
        """Resource 1: Available Network Bearer"""
        return [21]  # WLAN available
    
    def get_radio_signal_strength(self, instance_id):
        """Resource 2: Radio Signal Strength (dBm)"""
        return random.randint(-80, -30)
    
    def get_link_quality(self, instance_id):
        """Resource 3: Link Quality"""
        return random.randint(1, 5)
    
    def get_ip_addresses(self, instance_id):
        """Resource 4: IP Addresses"""
        return ["192.168.1.100"]
    
    def get_router_ip_address(self, instance_id):
        """Resource 5: Router IP Address"""
        return ["192.168.1.1"]
    
    def get_link_utilization(self, instance_id):
        """Resource 6: Link Utilization (%)"""
        return random.randint(10, 80)

# Factory function to create all standard objects
def create_standard_objects():
    """Create all standard LwM2M objects"""
    return {
        0: SecurityObject(),
        1: ServerObject(),
        3: DeviceObject(),
        4: ConnectivityMonitoringObject()
    }

# Resource definitions for proper LwM2M compliance
RESOURCE_DEFINITIONS = {
    0: {  # Security Object
        0: {"name": "LwM2M Server URI", "type": "string", "operations": "R"},
        1: {"name": "Bootstrap Server", "type": "boolean", "operations": "R"},
        2: {"name": "Security Mode", "type": "integer", "operations": "R"},
        3: {"name": "Public Key or Identity", "type": "opaque", "operations": "R"},
        4: {"name": "Server Public Key", "type": "opaque", "operations": "R"},
    },
    1: {  # Server Object
        0: {"name": "Short Server ID", "type": "integer", "operations": "R"},
        1: {"name": "Lifetime", "type": "integer", "operations": "RW"},
        2: {"name": "Default Minimum Period", "type": "integer", "operations": "RW"},
        3: {"name": "Default Maximum Period", "type": "integer", "operations": "RW"},
        6: {"name": "Notification Storing", "type": "boolean", "operations": "RW"},
        7: {"name": "Binding", "type": "string", "operations": "RW"},
    },
    3: {  # Device Object
        0: {"name": "Manufacturer", "type": "string", "operations": "R"},
        1: {"name": "Model Number", "type": "string", "operations": "R"},
        2: {"name": "Serial Number", "type": "string", "operations": "R"},
        3: {"name": "Firmware Version", "type": "string", "operations": "R"},
        4: {"name": "Reboot", "type": "none", "operations": "E"},
        9: {"name": "Battery Level", "type": "integer", "operations": "R"},
        10: {"name": "Memory Free", "type": "integer", "operations": "R"},
        11: {"name": "Error Code", "type": "integer", "operations": "R"},
        13: {"name": "Current Time", "type": "time", "operations": "RW"},
    },
    4: {  # Connectivity Monitoring
        0: {"name": "Network Bearer", "type": "integer", "operations": "R"},
        1: {"name": "Available Network Bearer", "type": "integer", "operations": "R"},
        2: {"name": "Radio Signal Strength", "type": "integer", "operations": "R"},
        3: {"name": "Link Quality", "type": "integer", "operations": "R"},
        4: {"name": "IP Addresses", "type": "string", "operations": "R"},
    }
}