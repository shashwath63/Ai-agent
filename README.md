# Full-Stack AI Development Agent

## Overview

This project implements an AI-powered assistant to help you create, manage, and improve full-stack applications via a terminal-based, step-by-step process. The agent works in cycles of **start, plan, action, observe** — enabling iterative and interactive software development. It accepts natural language requests, plans the approach, executes actions (using Python functions), and observes the results for the next step.

## Main Features
- **Project Generation**: Quickly create new projects using React, Vue, Node.js, Python Flask/Django, and more.
- **Code Editing and File Operations**: Easily create, read, write, or delete files and directories.
- **Dependency & Command Management**: Install dependencies, run scripts, and execute terminal commands.
- **Development Best Practices**: Enforces structured code generation, best practices, error handling, and documentation.
- **Context Awareness**: Reads existing files and directories to make context-aware changes.
- **Stepwise Output Format**: Responds in strict JSON format, ensuring traceability and easy tool integration.

## Modes and Workflow
- **start**: Initial user request.
- **plan**: Outlines approach and required steps.
- **action**: Executes a specific tool/function.
- **observe**: Reviews and summarizes the results of the action.

## Output JSON Format
Every response adheres to the following format:
```
{
  "step": "string",         // E.g., "plan", "action", "observe", "output"
  "content": "string",      // Explanation of what’s being done or the result
  "function": "string",     // Name of function/tool invoked (if step is action)
  "input": "string"         //## Advanced Usage Examples

### Multi-Step Development
You can chain features or requests step by step. For example:
1. `Create a Flask API project.`
2. `Add a /hello endpoint that returns JSON.`
3. `Set up basic tests and run them.`
4. `Add Docker support.`

The agent ensures each step is completed before moving to the next, providing maximum control over your build process.

### Automatic Context Awareness
Before making changes (such as adding a new page or API route), the assistant reads directory structure or file content to ensure the right insertion points and avoid duplication.

### Custom Modes and Theming
When generating frontends, you can specify modes:
- `Create a dashboard in dark mode with sidebar navigation.`
- `Use Material UI and light mode for register/login pages.`

---

## Troubleshooting & FAQ

- **Nothing happens after my request:** Ensure your requests are clear, and that the Python environment and dependencies are set up.
- **API errors:** Check your `.env` file for a valid OpenAI API key and network connectivity.
- **JSON format errors:** This tool expects/outputs JSON; if using in an automated pipeline, validate output at each step.
- **Permission issues:** Some file or directory operations may require additional permissions, especially on protected paths.

---

## Contributing

1. Fork and clone the repository.
2. Add your improvements (tools/functions, UI/CLI tweaks, documentation).
3. Ensure your code is Pythonic, well-commented, and follows the same stepwise JSON output pattern.
4. Submit a pull request with a clear description.

For major new tools, update this README with usage instructions.

---

## License

MIT License. See `LICENSE` file for details.

---

## Technical Architecture

- **Core Loop:**
  - Accepts text input or commands.
  - Runs through an LLM planning & tool-use loop using OpenAI GPT models.
  - Each LLM output must be a JSON object specifying next step (plan/action/observe/output).
  - The Python backend executes the requested action, observes results, and feeds back to the loop.
- **Adding Tools:**
  - To add a new tool, define its function and add it to `available_tools` in `fullstack-ai-agent.py`.
  - Ensure input/output structure matches expectations for seamless integration.

---

## Getting Started Quickly

1. Install Python dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your OpenAI API key (`OPENAI_API_KEY=sk-...`).
3. Run the agent: `python fullstack-ai-agent.py`
4. Start issuing requests. See "Example Usage" section above for inspiration!

