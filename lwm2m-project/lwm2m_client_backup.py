# lwm2m-project/lwm2m_client.py
"""
Real LwM2M Client Implementation
Performs actual LwM2M operations with OSI layer measurements
"""
import aiocoap
import asyncio
import json
import time
import random
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LwM2MClient:
    """Real LwM2M Client with OSI Layer Analysis"""
    
    def __init__(self, server_host="127.0.0.1", server_port=5683):
        self.server_host = server_host
        self.server_port = server_port
        self.server_uri = f"coap://{server_host}:{server_port}"
        self.endpoint_name = f"lwm2m-device-{random.randint(1000, 9999)}"
        self.context = None
        self.registration_location = None
        self.objects = {
            '0': ['0'],  # Security Object
            '1': ['0'],  # Server Object  
            '3': ['0'],  # Device Object
            '4': ['0']   # Connectivity Monitoring
        }
        
    async def initialize(self):
        """Initialize CoAP context (Layer 4 - Transport)"""
        logger.info("🔧 Initializing LwM2M Client...")
        start_time = time.time()
        
        self.context = await aiocoap.Context.create_client_context()
        
        init_time = (time.time() - start_time) * 1000
        logger.info(f"✅ Client initialized in {init_time:.2f}ms")
        
        return {
            'initialization_time_ms': init_time,
            'transport_protocol': 'CoAP/UDP',
            'client_endpoint': self.endpoint_name
        }
    
    async def perform_registration(self):
        """LwM2M Device Registration (Layer 5 - Session)"""
        logger.info("📝 Performing LwM2M Device Registration...")
        start_time = time.time()
        
        # Create registration payload (object links)
        object_links = []
        for obj_id, instances in self.objects.items():
            for instance_id in instances:
                object_links.append(f"</{obj_id}/{instance_id}>")
        
        payload = ','.join(object_links)
        lifetime = 86400  # 24 hours
        
        # Registration request
        uri = f"{self.server_uri}/rd?ep={self.endpoint_name}&lt={lifetime}&b=U"
        
        request = aiocoap.Message(
            code=aiocoap.POST,
            uri=uri,
            payload=payload.encode(),
            content_format=40  # Link format
        )
        
        try:
            response = await self.context.request(request).response
            registration_time = (time.time() - start_time) * 1000
            
            if response.code.is_successful():
                # Extract location from response
                if response.opt.location_path:
                    self.registration_location = '/'.join(response.opt.location_path)
                    logger.info(f"✅ Registration successful: {self.registration_location}")
                    logger.info(f"📊 Registration time: {registration_time:.2f}ms")
                    
                    return {
                        'success': True,
                        'registration_time_ms': registration_time,
                        'location': self.registration_location,
                        'payload_size_bytes': len(payload.encode()),
                        'response_code': str(response.code),
                        'lifetime_seconds': lifetime,
                        'objects_registered': len(object_links)
                    }
                else:
                    logger.error("Registration successful but no location provided")
                    return {'success': False, 'error': 'No location in response'}
            else:
                logger.error(f"Registration failed: {response.code}")
                return {
                    'success': False,
                    'registration_time_ms': registration_time,
                    'error_code': str(response.code)
                }
                
        except Exception as e:
            registration_time = (time.time() - start_time) * 1000
            logger.error(f"Registration error: {e}")
            return {
                'success': False,
                'registration_time_ms': registration_time,
                'error': str(e)
            }
    
    async def send_data_with_tlv(self):
        """Send data using TLV encoding (Layer 6 - Presentation)"""
        logger.info("📊 Sending data with TLV encoding...")
        start_time = time.time()
        
        # Create sensor data
        sensor_data = {
            'temperature': round(20 + random.uniform(-5, 15), 1),
            'humidity': round(40 + random.uniform(0, 40), 1),
            'battery_level': random.randint(20, 100),
            'signal_strength': random.randint(-100, -50)
        }
        
        # Encode to TLV format
        tlv_data = self._encode_to_tlv(sensor_data)
        
        # Send to device object
        if self.registration_location:
            uri = f"{self.server_uri}/{self.registration_location}/3/0"
            
            request = aiocoap.Message(
                code=aiocoap.PUT,
                uri=uri,
                payload=tlv_data,
                content_format=11542  # LwM2M TLV
            )
            
            try:
                response = await self.context.request(request).response
                send_time = (time.time() - start_time) * 1000
                
                raw_json_size = len(json.dumps(sensor_data).encode())
                compression_ratio = raw_json_size / len(tlv_data)
                
                logger.info(f"✅ Data sent successfully in {send_time:.2f}ms")
                logger.info(f"📊 Compression: {raw_json_size}B → {len(tlv_data)}B (ratio: {compression_ratio:.2f})")
                
                return {
                    'success': response.code.is_successful(),
                    'send_time_ms': send_time,
                    'raw_data_size_bytes': raw_json_size,
                    'tlv_encoded_size_bytes': len(tlv_data),
                    'compression_ratio': compression_ratio,
                    'encoding_efficiency': len(tlv_data) / raw_json_size,
                    'response_code': str(response.code),
                    'sensor_data': sensor_data
                }
                
            except Exception as e:
                send_time = (time.time() - start_time) * 1000
                logger.error(f"Data send error: {e}")
                return {
                    'success': False,
                    'send_time_ms': send_time,
                    'error': str(e)
                }
        else:
            logger.error("Cannot send data: Not registered")
            return {'success': False, 'error': 'Not registered'}
    
    async def discover_server_resources(self):
        """Discover server resources (Layer 7 - Application)"""
        logger.info("🔍 Discovering server resources...")
        start_time = time.time()
        
        request = aiocoap.Message(
            code=aiocoap.GET,
            uri=f"{self.server_uri}/.well-known/core"
        )
        
        try:
            response = await self.context.request(request).response
            discovery_time = (time.time() - start_time) * 1000
            
            if response.code.is_successful():
                resources_payload = response.payload.decode()
                resource_count = len(resources_payload.split(','))
                
                logger.info(f"✅ Discovery completed in {discovery_time:.2f}ms")
                logger.info(f"📊 Found {resource_count} resources")
                
                return {
                    'success': True,
                    'discovery_time_ms': discovery_time,
                    'resources_found': resource_count,
                    'resources_payload_size_bytes': len(response.payload),
                    'resources_list': resources_payload,
                    'response_code': str(response.code)
                }
            else:
                logger.error(f"Discovery failed: {response.code}")
                return {
                    'success': False,
                    'discovery_time_ms': discovery_time,
                    'error_code': str(response.code)
                }
                
        except Exception as e:
            discovery_time = (time.time() - start_time) * 1000
            logger.error(f"Discovery error: {e}")
            return {
                'success': False,
                'discovery_time_ms': discovery_time,
                'error': str(e)
            }
    
    async def perform_update(self):
        """Perform registration update (Layer 5 - Session)"""
        logger.info("🔄 Performing registration update...")
        start_time = time.time()
        
        if not self.registration_location:
            return {'success': False, 'error': 'Not registered'}
        
        request = aiocoap.Message(
            code=aiocoap.PUT,
            uri=f"{self.server_uri}/{self.registration_location}"
        )
        
        try:
            response = await self.context.request(request).response
            update_time = (time.time() - start_time) * 1000
            
            logger.info(f"✅ Update completed in {update_time:.2f}ms")
            
            return {
                'success': response.code.is_successful(),
                'update_time_ms': update_time,
                'response_code': str(response.code)
            }
            
        except Exception as e:
            update_time = (time.time() - start_time) * 1000
            logger.error(f"Update error: {e}")
            return {
                'success': False,
                'update_time_ms': update_time,
                'error': str(e)
            }
    
    def _encode_to_tlv(self, data):
        """Encode data to LwM2M TLV format (Layer 6 - Presentation)"""
        tlv_data = bytearray()
        resource_id = 0
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if isinstance(value, float):
                    # Float resource (4 bytes)
                    value_bytes = int(value * 100).to_bytes(4, byteorder='big', signed=True)
                    tlv_data.extend([0xC4, resource_id, 0x04])  # Type, ID, Length
                    tlv_data.extend(value_bytes)
                else:
                    # Integer resource (2 bytes for small values)
                    if -32768 <= value <= 32767:
                        value_bytes = value.to_bytes(2, byteorder='big', signed=True)
                        tlv_data.extend([0xC2, resource_id, 0x02])  # Type, ID, Length
                        tlv_data.extend(value_bytes)
                    else:
                        value_bytes = value.to_bytes(4, byteorder='big', signed=True)
                        tlv_data.extend([0xC4, resource_id, 0x04])  # Type, ID, Length
                        tlv_data.extend(value_bytes)
            elif isinstance(value, str):
                # String resource
                value_bytes = value.encode('utf-8')
                tlv_data.extend([0xC8, resource_id, len(value_bytes)])  # Type, ID, Length
                tlv_data.extend(value_bytes)
            
            resource_id += 1
        
        return bytes(tlv_data)
    
    async def close(self):
        """Close client connection"""
        if self.context:
            await self.context.shutdown()
            logger.info("🔌 LwM2M Client connection closed")

# Test function
async def test_lwm2m_client():
    """Test the LwM2M client with full operation cycle"""
    client = LwM2MClient()
    
    try:
        # Initialize
        init_result = await client.initialize()
        
        # Register
        registration_result = await client.perform_registration()
        
        if registration_result['success']:
            # Send data
            data_result = await client.send_data_with_tlv()
            
            # Discover resources  
            discovery_result = await client.discover_server_resources()
            
            # Update registration
            update_result = await client.perform_update()
            
            return {
                'initialization': init_result,
                'registration': registration_result,
                'data_transmission': data_result,
                'resource_discovery': discovery_result,
                'registration_update': update_result
            }
        else:
            return {
                'initialization': init_result,
                'registration': registration_result,
                'error': 'Registration failed'
            }
            
    finally:
        await client.close()

if __name__ == "__main__":
    results = asyncio.run(test_lwm2m_client())
    print("\n📊 LwM2M Client Test Results:")
    print(json.dumps(results, indent=2, default=str))