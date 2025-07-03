#!/usr/bin/env python3
"""
Test script to verify HermesAPI connectivity
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

async def test_hermes_api():
    """Test all HermesAPI endpoints"""
    load_dotenv()
    
    base_url = os.getenv('HERMES_API_BASE_URL', 'http://localhost:8080')
    api_key = os.getenv('HERMES_API_KEY', '')
    
    print(f"🧪 Testing HermesAPI at: {base_url}")
    print("=" * 50)
    
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
        print(f"🔑 Using API key: {api_key[:10]}...")
    
    async with aiohttp.ClientSession() as session:
        # Test player count endpoint
        try:
            print("📊 Testing /players/count...")
            async with session.get(f"{base_url}/players/count", headers=headers) as response:
                if response.status == 200:
                    count = await response.text()
                    print(f"   ✅ Success: {count.strip()} players online")
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test player names endpoint
        try:
            print("👥 Testing /players/names...")
            async with session.get(f"{base_url}/players/names", headers=headers) as response:
                if response.status == 200:
                    names = await response.text()
                    if names.strip():
                        players = [name.strip() for name in names.split(',')]
                        print(f"   ✅ Success: Players online: {', '.join(players)}")
                    else:
                        print("   ✅ Success: No players online")
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test SSE endpoint (brief connection)
        try:
            print("🔄 Testing /players/connections (SSE)...")
            async with session.get(f"{base_url}/players/connections", headers=headers) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'text/event-stream' in content_type:
                        print("   ✅ Success: SSE endpoint is accessible")
                        
                        # Read a small amount to test the stream
                        try:
                            chunk = await asyncio.wait_for(response.content.read(100), timeout=2.0)
                            print(f"   📡 Received data from stream")
                        except asyncio.TimeoutError:
                            print("   ⏱️  No immediate data (normal for SSE)")
                    else:
                        print(f"   ⚠️  Unexpected content type: {content_type}")
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test chat send endpoint
        try:
            print("💬 Testing /chat/send (POST)...")
            chat_payload = {
                'sender': '[Test] Test Bot',
                'message': 'This is a test message from the API test script'
            }
            async with session.post(
                f"{base_url}/chat/send",
                headers={**headers, 'Content-Type': 'application/json'},
                json=chat_payload
            ) as response:
                if response.status == 200:
                    print("   ✅ Success: Chat message sent successfully")
                elif response.status == 404:
                    print("   ⚠️  Chat endpoint not found (may not be implemented yet)")
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test chat stream endpoint
        try:
            print("💭 Testing /chat/stream (SSE)...")
            async with session.get(f"{base_url}/chat/stream", headers=headers) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'text/event-stream' in content_type:
                        print("   ✅ Success: Chat SSE endpoint is accessible")
                        
                        # Read a small amount to test the stream
                        try:
                            chunk = await asyncio.wait_for(response.content.read(100), timeout=2.0)
                            print(f"   📡 Received chat data from stream")
                        except asyncio.TimeoutError:
                            print("   ⏱️  No immediate chat data (normal for SSE)")
                    else:
                        print(f"   ⚠️  Unexpected content type: {content_type}")
                elif response.status == 404:
                    print("   ⚠️  Chat stream endpoint not found (may not be implemented yet)")
                else:
                    print(f"   ❌ Failed: HTTP {response.status}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎯 Test Summary:")
    print("✅ = Endpoint working correctly")
    print("⚠️  = Endpoint may not be implemented yet") 
    print("❌ = Error or connection issue")
    print("If you see ❌ for basic endpoints, check your Minecraft server and HermesAPI installation.")
    print("If you see ⚠️  for chat endpoints, the HermesAPI may not have chat features implemented yet.")

def main():
    """Main test function"""
    print("🚀 HermesAPI Connection Test")
    print("=" * 50)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ No .env file found!")
        print("💡 Run: python setup.py")
        return 1
    
    try:
        asyncio.run(test_hermes_api())
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 