# Example Usage Scenarios

## Scenario 1: React Development

```bash
# Starting a React development session
$ cl analyze "I need to build a React component with hooks and state management"

🔍 Tools needed for: 'I need to build a React component with...'
   - mcp:context7 (React documentation)
   - mcp:magic (UI component generation)
   - agent:frontend-developer

📦 Loading tools...
  ✅ Loaded MCP server: context7 (1.7k tokens)
  ✅ Loaded MCP server: magic (2.8k tokens)
  ✅ Loaded agent: frontend-developer (304 tokens)

Total loaded: 4.8k tokens (vs 108k traditional)
Savings: 103.2k tokens (95.6%)
```

## Scenario 2: WordPress Debugging

```bash
# Debugging WordPress issues
$ cl preload wordpress

📦 Preloading profile: wordpress
  ✅ Loaded MCP server: ssh-wordpress (6.5k tokens)
  ✅ Loaded MCP server: wordpress-tayloredfocus (5.8k tokens)
  ✅ Loaded agent: frontend-developer (304 tokens)

Total loaded: 12.6k tokens (vs 108k traditional)
Savings: 95.4k tokens (88.3%)
```

## Scenario 3: Complex System Analysis

```bash
# Analyzing complex architecture
$ cl analyze "analyze the complex microservices architecture for performance bottlenecks"

🔍 Tools needed for: 'analyze the complex microservices...'
   - mcp:sequential-thinking (complex analysis)
   - mcp:serena (code understanding)
   - agent:system-architect
   - agent:performance-engineer

📦 Loading tools...
  ✅ Loaded MCP server: sequential-thinking (1.3k tokens)
  ✅ Loaded MCP server: serena (9.2k tokens)
  ✅ Loaded agent: system-architect (27 tokens)
  ✅ Loaded agent: performance-engineer (24 tokens)

Total loaded: 10.6k tokens (vs 108k traditional)
Savings: 97.4k tokens (90.2%)
```

## Scenario 4: Simple Query (Maximum Savings)

```bash
# Simple question that needs no tools
$ cl analyze "explain what a variable is in Python"

✅ No additional tools needed

Total loaded: 5k tokens (registry only)
Savings: 103k tokens (95.4%)
```

## Scenario 5: Progressive Loading

```bash
# Start simple, load more as needed
$ cl stats
📊 Lazy Loading Statistics
Available: 10 MCP servers, 15 agents
Loaded: 0 MCP servers, 0 agents
Token usage: 5,000 tokens
Tokens saved: 103,000 (95.4%)

# User starts with React
$ cl analyze "create a React component"
  ✅ Loaded: context7, magic (4.5k tokens)

$ cl stats
Loaded: 2 MCP servers, 0 agents
Token usage: 9,500 tokens
Tokens saved: 98,500 (91.2%)

# User needs testing
$ cl analyze "now add tests for this component"
  ✅ Loaded: playwright, test-writer-fixer (11.6k tokens)

$ cl stats
Loaded: 4 MCP servers, 1 agent
Token usage: 21,100 tokens
Tokens saved: 86,900 (80.5%)

# Still 80% savings even with multiple tools loaded!
```

## Real Session Comparison

### Traditional Claude Code Session
```
/context
⛁ ⛀ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁  Context Usage
⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁  111k/200k tokens (56%)

Before any conversation even starts!
```

### With Lazy Loading
```
/context
⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁ ⛁  Context Usage
⛁ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶ ⛶  5k/200k tokens (2.5%)

195k tokens available for actual work!
```