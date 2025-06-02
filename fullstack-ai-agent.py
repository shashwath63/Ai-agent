from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import requests
import os
import pathlib
import subprocess

load_dotenv()
client = OpenAI()

def run_command(cmd: str):
    """Execute terminal/shell commands"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = f"Command: {cmd}\n"
        if result.stdout:
            output += f"Output: {result.stdout}\n"
        if result.stderr:
            output += f"Error: {result.stderr}\n"
        output += f"Return code: {result.returncode}"
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"

def get_weather(city: str):
    """Get current weather for a city"""
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

def create_file(file_path: str, content: str = ""):
    """Create a file with optional content"""
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ File '{file_path}' created successfully."
    except Exception as e:
        return f"❌ Error creating file: {str(e)}"

def read_file(file_path: str):
    """Read contents of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"📄 Contents of '{file_path}':\n{'-'*50}\n{content}\n{'-'*50}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

def create_directory(dir_path: str):
    """Create a directory structure"""
    try:
        os.makedirs(dir_path, exist_ok=True)
        return f"📁 Directory '{dir_path}' created successfully."
    except Exception as e:
        return f"❌ Error creating directory: {str(e)}"

def list_directory(dir_path: str = "."):
    """List contents of a directory"""
    try:
        items = []
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                items.append(f"📁 {item}/")
            else:
                items.append(f"📄 {item}")
        return f"📂 Contents of '{dir_path}':\n" + "\n".join(items)
    except Exception as e:
        return f"❌ Error listing directory: {str(e)}"

def write_to_file(file_path: str, content: str, mode: str = "w"):
    """Write to a file (w=overwrite, a=append)"""
    try:
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(content)
        action = "appended to" if mode == "a" else "written to"
        return f"✅ Content {action} '{file_path}' successfully."
    except Exception as e:
        return f"❌ Error writing to file: {str(e)}"

def read_project_structure(base_path: str = ".", max_depth: int = 3):
    """Get an overview of project structure"""
    try:
        structure = []

        def scan_directory(path, depth=0):
            if depth > max_depth:
                return

            try:
                items = sorted(os.listdir(path))
            except PermissionError:
                return

            for item in items:
                if item.startswith('.') and item not in ['.gitignore', '.env.example']:
                    continue

                item_path = os.path.join(path, item)
                indent = "  " * depth

                if os.path.isdir(item_path):
                    structure.append(f"{indent}📁 {item}/")
                    scan_directory(item_path, depth + 1)
                else:
                    # Show file size for better context
                    try:
                        size = os.path.getsize(item_path)
                        size_str = f" ({size} bytes)" if size < 1024 else f" ({size//1024}KB)"
                    except:
                        size_str = ""
                    structure.append(f"{indent}📄 {item}{size_str}")

        scan_directory(base_path)
        return f"🗂️  Project structure for '{base_path}':\n" + "\n".join(structure)
    except Exception as e:
        return f"❌ Error reading project structure: {str(e)}"

def find_files(pattern: str, base_path: str = "."):
    """Find files matching a pattern"""
    try:
        import glob
        matches = glob.glob(os.path.join(base_path, "**", pattern), recursive=True)
        if matches:
            return f"🔍 Found files matching '{pattern}':\n" + "\n".join(matches)
        else:
            return f"🔍 No files found matching '{pattern}'"
    except Exception as e:
        return f"❌ Error finding files: {str(e)}"

def copy_file(source: str, destination: str):
    """Copy a file from source to destination"""
    try:
        import shutil
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(destination)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(source, destination)
        return f"✅ File copied from '{source}' to '{destination}'"
    except Exception as e:
        return f"❌ Error copying file: {str(e)}"

def delete_file(file_path: str):
    """Delete a file"""
    try:
        os.remove(file_path)
        return f"🗑️  File '{file_path}' deleted successfully."
    except Exception as e:
        return f"❌ Error deleting file: {str(e)}"

def get_current_directory():
    """Get current working directory"""
    return f"📍 Current directory: {os.getcwd()}"

def change_directory(dir_path: str):
    """Change current working directory"""
    try:
        os.chdir(dir_path)
        return f"📍 Changed directory to: {os.getcwd()}"
    except Exception as e:
        return f"❌ Error changing directory: {str(e)}"

available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
    "create_file": create_file,
    "read_file": read_file,
    "create_directory": create_directory,
    "list_directory": list_directory,
    "write_to_file": write_to_file,
    "read_project_structure": read_project_structure,
    "find_files": find_files,
    "copy_file": copy_file,
    "delete_file": delete_file,
    "get_current_directory": get_current_directory,
    "change_directory": change_directory
}

SYSTEM_PROMPT = f"""
You are a specialized AI Assistant for coding and full-stack project development.
You work in start, plan, action, observe mode and operate entirely through the terminal.

Your specializations include:
- Creating full-stack projects (React, Vue, Node.js, Python Flask/Django, etc.)
- Generating proper folder and file structures following best practices
- Writing clean, production-ready code into appropriate files
- Managing dependencies (pip install, npm install, yarn add, etc.)
- Running build commands, tests, and development servers
- Understanding project context by reading existing files and structure
- Supporting iterative development with follow-up prompts
- Database setup and configuration
- API development and integration
- Frontend and backend architecture


Development Best Practices:
- Follow language-specific conventions and standards
- Create proper project structures (MVC, component-based, etc.)
- Include proper error handling and validation
- Add comments and documentation
- Set up proper environment configurations
- Include necessary dependencies and requirements
- Execute the commands to run the project and open browser as well by clicking on to the link
- Ask for the modes to generate the code (e.g., Dark mode, Light mode, etc.)

Rules:
- Follow the Output JSON Format exactly
- Always perform one step at a time and wait for next input
- When starting new projects, first understand requirements fully
- When modifying existing projects, first read relevant files to understand current state
- Create comprehensive project structures with all necessary folders
- Write complete, functional code (not just snippets)
- Include proper imports, exports, and configurations

Output JSON Format:
{{
 "step": "string",
 "content": "string",
 "function": "The name of function if the step is action",
 "input": "The input parameter(s) for the function (use | as delimiter for multiple params)"
}}

Available Tools:
- "get_weather": Get current weather (city)
- "run_command": Execute terminal commands (command)
- "create_file": Create new file with content (file_path|content)
- "read_file": Read file contents (file_path)
- "create_directory": Create directory structure (dir_path)
- "list_directory": List directory contents (dir_path)
- "write_to_file": Write/append to file (file_path|content|mode)
- "read_project_structure": Get project overview (base_path|max_depth)
- "find_files": Find files by pattern (pattern|base_path)
- "copy_file": Copy file (source|destination)
- "delete_file": Delete file (file_path)
- "get_current_directory": Get current working directory
- "change_directory": Change working directory (dir_path)

Examples:

User: Create a React app with login functionality
Assistant: {{ "step": "plan", "content": "I'll create a React app with login functionality. Steps: 1) Create project structure 2) Set up React with Vite/CRA 3) Create login component 4) Add routing 5) Set up basic styling" }}

User: Add a registration page to the existing app
Assistant: {{ "step": "plan", "content": "User wants to add registration to existing project. I should first check the current project structure to understand the layout and existing components." }}
Assistant: {{ "step": "action", "function": "read_project_structure", "input": "." }}

User: Install Express.js and create a basic API server
Assistant: {{ "step": "plan", "content": "I'll set up Express.js server. Steps: 1) Check if package.json exists 2) Install Express 3) Create server structure 4) Set up basic routes 5) Add middleware" }}
"""

def parse_tool_input(tool_name: str, tool_input: str):
    """Parse tool input based on the tool requirements"""
    if "|" in tool_input:
        params = [param.strip() for param in tool_input.split("|")]
    else:
        params = [tool_input.strip()]

    # Handle different tools and their parameter requirements
    if tool_name in ["create_file", "write_to_file"]:
        if len(params) >= 2:
            if tool_name == "write_to_file" and len(params) >= 3:
                return params[0], params[1], params[2]  # file_path, content, mode
            return params[0], params[1]  # file_path, content
        return params[0], ""  # file_path, empty content

    elif tool_name == "copy_file":
        if len(params) >= 2:
            return params[0], params[1]  # source, destination
        return params[0], params[0] + "_copy"  # default destination

    elif tool_name == "read_project_structure":
        if len(params) >= 2:
            return params[0], int(params[1]) if params[1].isdigit() else 3
        return params[0] if params else ".", 3

    elif tool_name == "find_files":
        if len(params) >= 2:
            return params[0], params[1]
        return params[0], "."

    else:
        return params[0] if params else ""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("🚀 Full-Stack Development AI Agent")
print("I can help you build complete web applications, APIs, and manage projects!")
print("Examples: 'Create a React todo app', 'Add authentication to my API', 'Set up a Python Flask server'")
print("=" * 80)

while True:
    query = input("\n💻 > ")
    if query.lower() in ['exit', 'quit', 'bye', 'exit()', 'quit()']:
        print("👋 Goodbye! Happy coding!")
        break

    if query.lower() in ['help', '?']:
        print("""
🔧 Available Commands:
- Project Creation: "Create a [framework] app with [features]"
- Feature Addition: "Add [feature] to my project"
- File Operations: "Read [filename]", "Create [filename] with [content]"
- Commands: "Install [package]", "Run [command]"
- Structure: "Show project structure", "List files"
- Navigation: "Change to [directory]", "Show current directory"
        """)
        continue

    messages.append({"role": "user", "content": query})

    step_count = 0
    max_steps = 20  # Prevent infinite loops

    while step_count < max_steps:
        try:
            # Try with JSON mode first, fallback if not supported
            try:
                response = client.chat.completions.create(
                    model="gpt-4.1",  # Use gpt-4o which supports JSON mode
                    response_format={"type": "json_object"},
                    messages=messages
                )
            except Exception as json_error:
                # Fallback to regular mode without JSON formatting
                print("⚠️  JSON mode not supported, using regular mode...")
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Fallback model
                    messages=messages
                )

                # Try to extract JSON from the response
                content = response.choices[0].message.content
                # Look for JSON-like content in the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    content = json_match.group()
                else:
                    # Create a default response if no JSON found
                    content = '{"step": "output", "content": "' + content.replace('"', '\\"') + '"}'

            content = response.choices[0].message.content
            messages.append({"role": "assistant", "content": content})
            parsed_response = json.loads(content)

            step = parsed_response.get("step")
            step_content = parsed_response.get("content", "")

            if step == "plan":
                print(f"🧠 Planning: {step_content}")
                step_count += 1
                continue

            elif step == "action":
                tool_name = parsed_response.get("function")
                tool_input = parsed_response.get("input", "")
                print(f"🛠️  Executing: {tool_name}")

                if tool_name in available_tools:
                    try:
                        # Parse input parameters based on tool requirements
                        parsed_params = parse_tool_input(tool_name, tool_input)

                        if isinstance(parsed_params, tuple):
                            output = available_tools[tool_name](*parsed_params)
                        else:
                            output = available_tools[tool_name](parsed_params)

                        messages.append({"role": "user", "content": json.dumps({"step": "observe", "output": output})})

                    except Exception as e:
                        error_msg = f"❌ Error executing {tool_name}: {str(e)}"
                        print(error_msg)
                        messages.append({"role": "user", "content": json.dumps({"step": "observe", "output": error_msg})})
                else:
                    error_msg = f"❌ Tool '{tool_name}' not available"
                    print(error_msg)
                    break

                step_count += 1
                continue

            elif step == "observe":
                print(f"👀 Observing: {step_content}")
                step_count += 1
                continue

            elif step == "output":
                print(f"✅ Result: {step_content}")
                break

            else:
                print(f"🤖 {step_content}")
                break

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break

    if step_count >= max_steps:
        print("⚠️  Maximum steps reached. Please try a simpler request or break it into smaller tasks.")
