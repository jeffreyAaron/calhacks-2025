"""
MCP Client for Browser MCP Server
Connects to the browser MCP server and provides browser control tools
"""
import subprocess
import json
import asyncio
from typing import Dict, List, Optional, Any


class BrowserMCPClient:
    """Client for Browser MCP server"""
    
    def __init__(self):
        self.process = None
        self.connected = False
        
    async def start(self):
        """Start the browser MCP server"""
        print("🚀 Starting Browser MCP server...")
        
        # Start the MCP server process
        self.process = await asyncio.create_subprocess_exec(
            'npx',
            '@browsermcp/mcp@latest',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        self.connected = True
        print("✅ Browser MCP server started")
        
    async def stop(self):
        """Stop the browser MCP server"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            self.connected = False
            print("🛑 Browser MCP server stopped")
    
    async def send_request(self, method: str, params: Dict = None) -> Dict:
        """
        Send a request to the MCP server
        
        Args:
            method: The MCP method to call
            params: Parameters for the method
            
        Returns:
            Response from the server
        """
        if not self.connected:
            raise RuntimeError("MCP server not connected")
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        # Send request
        request_json = json.dumps(request) + '\n'
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode())
        
        return response
    
    async def navigate(self, url: str) -> Dict:
        """Navigate to a URL"""
        return await self.send_request("tools/call", {
            "name": "browser_navigate",
            "arguments": {"url": url}
        })
    
    async def snapshot(self) -> Dict:
        """Get page snapshot"""
        return await self.send_request("tools/call", {
            "name": "browser_snapshot",
            "arguments": {}
        })
    
    async def click(self, element: str, ref: str) -> Dict:
        """Click an element"""
        return await self.send_request("tools/call", {
            "name": "browser_click",
            "arguments": {
                "element": element,
                "ref": ref
            }
        })
    
    async def type_text(self, element: str, ref: str, text: str, submit: bool = False) -> Dict:
        """Type text into an element"""
        return await self.send_request("tools/call", {
            "name": "browser_type",
            "arguments": {
                "element": element,
                "ref": ref,
                "text": text,
                "submit": submit
            }
        })
    
    async def select_option(self, element: str, ref: str, values: List[str]) -> Dict:
        """Select option in dropdown"""
        return await self.send_request("tools/call", {
            "name": "browser_select_option",
            "arguments": {
                "element": element,
                "ref": ref,
                "values": values
            }
        })
    
    async def press_key(self, key: str) -> Dict:
        """Press a keyboard key"""
        return await self.send_request("tools/call", {
            "name": "browser_press_key",
            "arguments": {"key": key}
        })
    
    async def wait(self, time: float) -> Dict:
        """Wait for a specified time"""
        return await self.send_request("tools/call", {
            "name": "browser_wait",
            "arguments": {"time": time}
        })
    
    async def screenshot(self) -> Dict:
        """Take a screenshot"""
        return await self.send_request("tools/call", {
            "name": "browser_screenshot",
            "arguments": {}
        })
    
    async def get_console_logs(self) -> Dict:
        """Get browser console logs"""
        return await self.send_request("tools/call", {
            "name": "browser_get_console_logs",
            "arguments": {}
        })


# Synchronous wrapper for easier use
class BrowserMCPSync:
    """Synchronous wrapper for BrowserMCPClient"""
    
    def __init__(self):
        self.client = BrowserMCPClient()
        self.loop = None
        
    def start(self):
        """Start the browser MCP server"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.client.start())
        
    def stop(self):
        """Stop the browser MCP server"""
        if self.loop:
            self.loop.run_until_complete(self.client.stop())
            self.loop.close()
    
    def navigate(self, url: str) -> Dict:
        """Navigate to a URL"""
        return self.loop.run_until_complete(self.client.navigate(url))
    
    def snapshot(self) -> Dict:
        """Get page snapshot"""
        return self.loop.run_until_complete(self.client.snapshot())
    
    def click(self, element: str, ref: str) -> Dict:
        """Click an element"""
        return self.loop.run_until_complete(self.client.click(element, ref))
    
    def type_text(self, element: str, ref: str, text: str, submit: bool = False) -> Dict:
        """Type text into an element"""
        return self.loop.run_until_complete(self.client.type_text(element, ref, text, submit))
    
    def select_option(self, element: str, ref: str, values: List[str]) -> Dict:
        """Select option in dropdown"""
        return self.loop.run_until_complete(self.client.select_option(element, ref, values))
    
    def press_key(self, key: str) -> Dict:
        """Press a keyboard key"""
        return self.loop.run_until_complete(self.client.press_key(key))
    
    def wait(self, time: float) -> Dict:
        """Wait for a specified time"""
        return self.loop.run_until_complete(self.client.wait(time))
    
    def screenshot(self) -> Dict:
        """Take a screenshot"""
        return self.loop.run_until_complete(self.client.screenshot())
    
    def get_console_logs(self) -> Dict:
        """Get browser console logs"""
        return self.loop.run_until_complete(self.client.get_console_logs())


if __name__ == '__main__':
    # Test the MCP client
    async def test():
        client = BrowserMCPClient()
        
        try:
            await client.start()
            
            # Test navigation
            print("\n📍 Testing navigation...")
            result = await client.navigate("https://www.google.com")
            print(f"Result: {result}")
            
            # Test snapshot
            print("\n📸 Testing snapshot...")
            result = await client.snapshot()
            print(f"Result: {json.dumps(result, indent=2)[:500]}...")
            
        finally:
            await client.stop()
    
    print("🧪 Testing Browser MCP Client")
    asyncio.run(test())

