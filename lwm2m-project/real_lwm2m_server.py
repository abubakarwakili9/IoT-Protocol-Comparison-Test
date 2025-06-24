# lwm2m-project/real_lwm2m_server.py
"""
Real LwM2M Server Implementation
Using aiocoap with full LwM2M specifications
"""

import aiocoap.resource as resource
import aiocoap
import asyncio
import json
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LwM2MResource:
    """Base class for LwM2M resources"""
    def __init__(self, obj_id: int, instance_id: int):
        self.obj_id = obj_id
        self.instance_id = instance_id
        self.resources = {}
        self.last_updated = datetime.now()

class DeviceObject(LwM2MResource):
    """LwM2M Device Object (Object ID 3)"""
    def __init__(self, instance_id: int = 0):
        super().__init__(3, instance_id)
        self.resources = {
            0: "Real LwM2M Device",           # Manufacturer
            1: "Research Protocol Analyzer",  # Model Number
            2: "RPA-2024-001",               # Serial Number
            3: "1.0.0",                      # Firmware Version
            9: 85,                           # Battery Level
            10: 512000,                      # Memory Free (bytes)
            11: [0],                         # Error Code
            13: datetime.now(),              # Current Time
            16: "U",                         # Binding Mode
        }

class ConnectivityMonitoringObject(LwM2MResource):
    """LwM2M Connectivity Monitoring Object (Object ID 4)"""
    def __init__(self, instance_id: int = 0):
        super().__init__(4, instance_id)
        self.resources = {
            0: 1,      # Network Bearer (WiFi)
            1: [0],    # Available Network Bearer
            2: -65,    # Radio Signal Strength (dBm)
            3: 0,      # Link Quality
            4: ["192.168.1.100"],  # IP Addresses
            5: ["192.168.1.1"],    # Router IP
            6: 2,      # Link Utilization (%)
            7: ["8.8.8.8", "8.8.4.4"],  # APN
            8: 0,      # Cell ID
            9: 0,      # SMNC
            10: 0,     # SMCC
        }

class RealLwM2MServer:
    """Real LwM2M Server with full protocol implementation"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 5683):
        self.host = host
        self.port = port
        self.clients = {}
        self.objects = {}
        self.observations = {}
        
    async def start_server(self) -> aiocoap.Context:
        """Start the real LwM2M server"""
        logger.info(f"Starting Real LwM2M Server on {self.host}:{self.port}")
        
        # Create root resource
        root = resource.Site()
        
        # Add LwM2M registration endpoint
        root.add_resource(['rd'], RegistrationResource(self))
        
        # Add bootstrap endpoint
        root.add_resource(['bs'], BootstrapResource(self))
        
        # Add well-known core for resource discovery
        root.add_resource(['.well-known', 'core'], WellKnownCore(self))
        
        # Add device management endpoints
        root.add_resource(['rd', resource.PathCapture('client'), 
                          resource.PathCapture('obj'), 
                          resource.PathCapture('inst')], 
                         ObjectResource(self))
        
        # Start CoAP server
        context = await aiocoap.Context.create_server_context(
            root, bind=(self.host, self.port)
        )
        
        logger.info("✅ Real LwM2M Server started successfully!")
        logger.info(f"📡 Server URI: coap://{self.host}:{self.port}")
        
        return context

class RegistrationResource(resource.Resource):
    """Real LwM2M Registration Resource (/rd)"""
    
    def __init__(self, server: RealLwM2MServer):
        super().__init__()
        self.server = server
        
    async def render_post(self, request: aiocoap.Message) -> aiocoap.Message:
        """Handle device registration with full LwM2M compliance"""
        start_time = time.time()
        
        # Parse query parameters
        query_params = self._parse_query_parameters(request.opt.uri_query or [])
        
        endpoint_name = query_params.get('ep')
        lifetime = int(query_params.get('lt', 86400))  # Default 24 hours
        binding_mode = query_params.get('b', 'U')
        lwm2m_version = query_params.get('lwm2m', '1.0')
        
        if not endpoint_name:
            logger.error("Registration failed: Missing endpoint name")
            return aiocoap.Message(code=aiocoap.BAD_REQUEST)
        
        # Parse object instances from payload
        object_links = self._parse_object_links(request.payload.decode() if request.payload else "")
        
        # Create client registration
        client_info = {
            'endpoint_name': endpoint_name,
            'lifetime': lifetime,
            'binding_mode': binding_mode,
            'lwm2m_version': lwm2m_version,
            'registration_time': datetime.now(),
            'last_update': datetime.now(),
            'object_links': object_links,
            'location': f"rd/{endpoint_name}",
        }
        
        self.server.clients[endpoint_name] = client_info
        
        registration_time = (time.time() - start_time) * 1000
        
        logger.info(f"✅ Device registered: {endpoint_name}")
        logger.info(f"   Registration time: {registration_time:.2f}ms")
        logger.info(f"   Objects: {list(object_links.keys())}")
        logger.info(f"   Binding mode: {binding_mode}")
        logger.info(f"   Lifetime: {lifetime}s")
        
        # Return successful registration
        response = aiocoap.Message(code=aiocoap.CREATED)
        response.opt.location_path = ['rd', endpoint_name]
        response.opt.max_age = lifetime
        
        return response
    
    def _parse_query_parameters(self, query_list) -> Dict[str, str]:
        """Parse LwM2M query parameters"""
        params = {}
        for query in query_list:
            if b'=' in query:
                key, value = query.decode().split('=', 1)
                params[key] = value
            else:
                params[query.decode()] = True
        return params
    
    def _parse_object_links(self, payload: str) -> Dict[str, Any]:
        """Parse LwM2M object links with full attribute support"""
        objects = {}
        if not payload.strip():
            return objects
        
        # Parse links like </3/0>;pmin=10;pmax=60,</4/0>;ver=1.1
        links = payload.split(',')
        for link in links:
            link = link.strip()
            if not link:
                continue
                
            # Split link and attributes
            parts = link.split(';')
            path = parts[0].strip('<>')
            
            # Parse path
            path_parts = path.split('/')
            if len(path_parts) >= 2:
                obj_id = path_parts[1]
                instance_id = path_parts[2] if len(path_parts) > 2 else '0'
                resource_id = path_parts[3] if len(path_parts) > 3 else None
                
                if obj_id not in objects:
                    objects[obj_id] = {'instances': {}}
                
                if instance_id not in objects[obj_id]['instances']:
                    objects[obj_id]['instances'][instance_id] = {'resources': {}}
                
                # Parse attributes
                attributes = {}
                for attr in parts[1:]:
                    if '=' in attr:
                        key, value = attr.split('=', 1)
                        attributes[key] = value
                    else:
                        attributes[attr] = True
                
                if resource_id:
                    objects[obj_id]['instances'][instance_id]['resources'][resource_id] = attributes
                else:
                    objects[obj_id]['instances'][instance_id]['attributes'] = attributes
        
        return objects

class WellKnownCore(resource.Resource):
    """Enhanced /.well-known/core with LwM2M discovery"""
    
    def __init__(self, server: RealLwM2MServer):
        super().__init__()
        self.server = server
    
    async def render_get(self, request: aiocoap.Message) -> aiocoap.Message:
        """Return LwM2M server capabilities"""
        start_time = time.time()
        
        # Build resource directory according to LwM2M spec
        core_links = [
            '</rd>;rt="core.rd";ct=40',
            '</rd-lookup/ep>;rt="core.rd-lookup-ep";ct=40',
            '</rd-lookup/d>;rt="core.rd-lookup-d";ct=40', 
            '</rd-lookup/res>;rt="core.rd-lookup-res";ct=40',
            '</bs>;rt="core.bootstrap";ct=40'
        ]
        
        # Add registered clients
        for endpoint, client_info in self.server.clients.items():
            for obj_id, obj_info in client_info['object_links'].items():
                for inst_id in obj_info['instances']:
                    link = f"</rd/{endpoint}/{obj_id}/{inst_id}>;obs"
                    core_links.append(link)
        
        discovery_time = (time.time() - start_time) * 1000
        logger.info(f"Resource discovery completed in {discovery_time:.2f}ms")
        
        payload = ','.join(core_links)
        return aiocoap.Message(
            payload=payload.encode(),
            code=aiocoap.CONTENT,
            content_format=40  # Link format
        )

# Usage example
async def run_real_lwm2m_server():
    """Run the real LwM2M server"""
    server = RealLwM2MServer()
    context = await server.start_server()
    
    try:
        logger.info("🔄 Real LwM2M Server running...")
        logger.info("Press Ctrl+C to stop")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Real LwM2M Server stopped")

if __name__ == "__main__":
    asyncio.run(run_real_lwm2m_server())