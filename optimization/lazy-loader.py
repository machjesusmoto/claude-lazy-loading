#!/usr/bin/env python3
"""
Lazy loader for Claude tools - reduces context by loading only what's needed.
This should be integrated into Claude's startup sequence.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

class ClaudeLazyLoader:
    def __init__(self):
        self.registry_path = Path.home() / ".claude" / "optimization" / "tool-registry.json"
        self.loaded_tools: Set[str] = set()
        self.registry: Dict = {}
        self.load_registry()
    
    def load_registry(self):
        """Load the tool registry."""
        if not self.registry_path.exists():
            print(f"⚠️  Registry not found at {self.registry_path}")
            print("   Run: python3 ~/.claude/optimization/generate-index.py")
            sys.exit(1)
        
        with open(self.registry_path) as f:
            self.registry = json.load(f)
    
    def analyze_input(self, user_input: str) -> List[str]:
        """Analyze user input to determine which tools to load."""
        tools_to_load = []
        input_lower = user_input.lower()
        
        # Check MCP servers
        for server_name, server_info in self.registry.get("mcp_servers", {}).items():
            if server_name in self.loaded_tools:
                continue
            
            # Check trigger keywords
            for keyword in server_info.get("trigger_keywords", []):
                if keyword.lower() in input_lower:
                    tools_to_load.append(f"mcp:{server_name}")
                    break
        
        # Check custom agents
        for agent_name, agent_info in self.registry.get("custom_agents", {}).items():
            if agent_name in self.loaded_tools:
                continue
            
            # Check trigger keywords
            for keyword in agent_info.get("trigger_keywords", []):
                if keyword.lower() in input_lower:
                    tools_to_load.append(f"agent:{agent_name}")
                    break
        
        # Check for specific commands
        command_patterns = {
            r"/analyze": ["mcp:sequential-thinking", "mcp:serena"],
            r"/build.*ui|/ui|/21": ["mcp:magic", "agent:frontend-developer"],
            r"/test": ["mcp:playwright", "agent:test-writer-fixer"],
            r"wordpress|tayloredfocus": ["mcp:ssh-wordpress", "mcp:wordpress-tayloredfocus"],
            r"import.*from|require\(": ["mcp:context7"],
            r"security|audit|vulnerability": ["agent:security-engineer", "mcp:sequential-thinking"],
            r"document|readme|guide": ["agent:technical-writer", "mcp:context7"]
        }
        
        for pattern, tools in command_patterns.items():
            if re.search(pattern, input_lower):
                tools_to_load.extend(tools)
        
        # Remove duplicates and already loaded
        tools_to_load = list(set(tools_to_load) - self.loaded_tools)
        
        return tools_to_load
    
    def load_tools(self, tools: List[str]) -> Dict:
        """Load specified tools and return their configurations."""
        loaded_configs = {}
        
        for tool in tools:
            tool_type, tool_name = tool.split(":", 1)
            
            if tool_type == "mcp":
                # Load MCP server configuration
                if tool_name in self.registry.get("mcp_servers", {}):
                    loaded_configs[tool] = {
                        "type": "mcp_server",
                        "name": tool_name,
                        "config": self.registry["mcp_servers"][tool_name]
                    }
                    self.loaded_tools.add(tool)
                    print(f"  ✅ Loaded MCP server: {tool_name}")
            
            elif tool_type == "agent":
                # Load custom agent configuration
                if tool_name in self.registry.get("custom_agents", {}):
                    loaded_configs[tool] = {
                        "type": "custom_agent",
                        "name": tool_name,
                        "config": self.registry["custom_agents"][tool_name]
                    }
                    self.loaded_tools.add(tool)
                    print(f"  ✅ Loaded agent: {tool_name}")
        
        return loaded_configs
    
    def get_stats(self) -> Dict:
        """Get current loading statistics."""
        total_mcp = len(self.registry.get("mcp_servers", {}))
        total_agents = len(self.registry.get("custom_agents", {}))
        loaded_mcp = sum(1 for t in self.loaded_tools if t.startswith("mcp:"))
        loaded_agents = sum(1 for t in self.loaded_tools if t.startswith("agent:"))
        
        return {
            "total_available": {
                "mcp_servers": total_mcp,
                "custom_agents": total_agents
            },
            "currently_loaded": {
                "mcp_servers": loaded_mcp,
                "custom_agents": loaded_agents
            },
            "loaded_tools": list(self.loaded_tools),
            "token_savings": self._estimate_token_savings()
        }
    
    def _estimate_token_savings(self) -> Dict:
        """Estimate token savings from lazy loading."""
        # Base registry size
        base_tokens = 5000
        
        # Add loaded tool tokens
        loaded_tokens = 0
        for tool in self.loaded_tools:
            tool_type, tool_name = tool.split(":", 1)
            if tool_type == "mcp":
                server_info = self.registry.get("mcp_servers", {}).get(tool_name, {})
                loaded_tokens += server_info.get("token_cost", 1000)
            elif tool_type == "agent":
                agent_info = self.registry.get("custom_agents", {}).get(tool_name, {})
                loaded_tokens += agent_info.get("token_cost", 100)
        
        # Calculate savings
        max_tokens = 108000  # Original load
        current_tokens = base_tokens + loaded_tokens
        saved_tokens = max_tokens - current_tokens
        
        return {
            "current_usage": current_tokens,
            "tokens_saved": saved_tokens,
            "percentage_saved": round((saved_tokens / max_tokens) * 100, 1)
        }
    
    def preload_profile(self, profile: str):
        """Preload tools for common workflows."""
        profiles = {
            "wordpress": [
                "mcp:ssh-wordpress",
                "mcp:wordpress-tayloredfocus",
                "agent:frontend-developer"
            ],
            "react": [
                "mcp:context7",
                "mcp:magic",
                "agent:frontend-developer",
                "agent:test-writer-fixer"
            ],
            "testing": [
                "mcp:playwright",
                "agent:test-writer-fixer",
                "agent:quality-engineer"
            ],
            "security": [
                "agent:security-engineer",
                "mcp:sequential-thinking",
                "agent:legal-compliance-checker"
            ],
            "backend": [
                "agent:backend-architect",
                "mcp:context7",
                "mcp:sequential-thinking"
            ]
        }
        
        if profile in profiles:
            tools = profiles[profile]
            print(f"📦 Preloading profile: {profile}")
            self.load_tools(tools)
        else:
            print(f"❌ Unknown profile: {profile}")
            print(f"   Available: {', '.join(profiles.keys())}")


def main():
    """CLI interface for the lazy loader."""
    loader = ClaudeLazyLoader()
    
    if len(sys.argv) < 2:
        print("Usage: lazy-loader.py <command> [args]")
        print("Commands:")
        print("  analyze <input>  - Analyze input and suggest tools")
        print("  load <tools>     - Load specific tools (comma-separated)")
        print("  preload <profile> - Load profile (wordpress/react/testing/security/backend)")
        print("  stats            - Show loading statistics")
        return
    
    command = sys.argv[1]
    
    if command == "analyze":
        if len(sys.argv) < 3:
            print("Usage: lazy-loader.py analyze <user_input>")
            return
        
        user_input = " ".join(sys.argv[2:])
        tools = loader.analyze_input(user_input)
        
        if tools:
            print(f"🔍 Tools needed for: '{user_input[:50]}...'")
            for tool in tools:
                print(f"   - {tool}")
            
            print("\n📦 Loading tools...")
            loader.load_tools(tools)
        else:
            print("✅ No additional tools needed")
    
    elif command == "load":
        if len(sys.argv) < 3:
            print("Usage: lazy-loader.py load <tool1,tool2,...>")
            return
        
        tools = sys.argv[2].split(",")
        print(f"📦 Loading {len(tools)} tools...")
        loader.load_tools(tools)
    
    elif command == "preload":
        if len(sys.argv) < 3:
            print("Usage: lazy-loader.py preload <profile>")
            return
        
        profile = sys.argv[2]
        loader.preload_profile(profile)
    
    elif command == "stats":
        stats = loader.get_stats()
        print("📊 Lazy Loading Statistics")
        print("=" * 40)
        print(f"Available: {stats['total_available']['mcp_servers']} MCP servers, "
              f"{stats['total_available']['custom_agents']} agents")
        print(f"Loaded: {stats['currently_loaded']['mcp_servers']} MCP servers, "
              f"{stats['currently_loaded']['custom_agents']} agents")
        print(f"Token usage: {stats['token_savings']['current_usage']:,} tokens")
        print(f"Tokens saved: {stats['token_savings']['tokens_saved']:,} "
              f"({stats['token_savings']['percentage_saved']}%)")
        
        if stats['loaded_tools']:
            print("\nCurrently loaded:")
            for tool in stats['loaded_tools']:
                print(f"  - {tool}")
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()