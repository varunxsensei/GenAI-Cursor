from openai import OpenAI
from dotenv import load_dotenv
import os
import json

session_state = {
    "files_created": [],
    "files_deleted": [],
    "history": []
}

def run_command(command):
    try:
        session_state["history"].append(command)  

        if command.strip().startswith("touch"):
            
            filename = command.strip().split()[1]
            open(filename, 'w').close()
            session_state["files_created"].append(filename)
            return f"✅ Created file: {filename}"

        elif command.strip().startswith("rm"):
            
            filename = command.strip().split()[1]
            if os.path.exists(filename):
                os.remove(filename)
                session_state["files_deleted"].append(filename)
                return f"🗑️ Deleted file: {filename}"
            else:
                return f"❌ File not found: {filename}"

        elif "open(" in command and "'w'" in command:
            
            start = command.find("open(")
            fname = command[start+5:].split(',')[0].strip(" ('\")")
            open(fname, 'w').close()
            session_state["files_created"].append(fname)
            return f"✅ Created file: {fname}"

        else:
            
            return os.system(command)

    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_created_files(_=None):
    if not session_state["files_created"]:
        return "No files have been created in this session."
    return "Files created:\n" + "\n".join(session_state["files_created"])

def get_deleted_files(_=None):
    if not session_state["files_deleted"]:
        return "No files have been deleted in this session."
    return "Files deleted:\n" + "\n".join(session_state["files_deleted"])

def get_command_history(_=None):
    if not session_state["history"]:
        return "No commands have been run yet."
    return "Command history:\n" + "\n".join(session_state["history"])


load_dotenv()

client = OpenAI()

available_tools = {
    "run_command": {
        "fn":run_command,
        "desc":"Takes a command as an input to execute on system and return output."
    },
    "get_created_files": {
        "fn": get_created_files,
        "desc": "Returns a list of all files created in this session."
    },
    "get_deleted_files": {
        "fn": get_deleted_files,
        "desc": "Returns list of all files deleted in this session."
    },
    "get_command_history": {
        "fn": get_command_history,
        "desc": "Returns history of all commands executed."
    }
}

system_prompt = """
You are a very smart AI Assistant who helps coder/programmers in there coding projects or error that they come across.You are specialised in linus,windows and macOS and are familier with all of the recent tech stack.
You work on start, plan, action, observe mode.
For the given user query and available tools, plan the step by step execution, based on the planning, select the relevant tool from the available tools, and based on the tool selection you perform an action to call the tool. Wait for the observation, and based on the observation resolve the user query.To solve the specific query you can also interact with user and ask problem specific questions to solve that problem more quickly.

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next step.
3. Carefully analyse the user query.

Output format:
{{"step":string,
  "content":string,
  "function":"The name of the function if the step is action",
  "input":"The input parameter for the function"
}}

Available Tools:
1. run_command : Takes a command as an input to execute on system and return output.
2. get_created_files: Returns a list of all files created in this session.
3. get_deleted_files: Returns list of all files deleted in this session.
4. get_command_history: Returns history of all commands executed.
    

Example 1:
User input :- What is the command for creating a new virtual environment in python.

Output:- {{"step":"plan","content":"The user is asking for a command to create a virtual environment"}}
Output:- {{"step": "plan","content":"Could you tell me which operating system you're using? (e.g., Windows, macOS, Linux)"}}
Output:- {{"step": "observe", "content": "Wait for the user to provide the operating system (e.g., Windows, macOS, Linux)."}}
Output:- {{"step":"output","content":"python3 -m venv venv"}}

Example 2:
User input :- Create a file with a name "hello.txt" in the current directory.

Output:- {{"step":"plan","content":"The user is asking to create a file in the current directory."}}
Output:- {{"step": "plan","content":"From the available tools i should call run_command function."}}
Output:- {{"step": "action", "function": "run_command","input":"touch hello.txt"}}
Output:- {{"step":"output","content":"created a 'hello.txt' file."}}
"""
messages = [
    {"role":"system","content":system_prompt}
]


while True:
    user_query = input("> ")
    if user_query.strip().lower() in ["quit", "exit"]:
        print("👋 Exiting assistant.")
        break
    while True:
        messages.append({"role":"user","content":user_query})
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type":"json_object"},
            messages=messages
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({"role":"assistant","content":json.dumps(parsed_response)})

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            if available_tools.get(tool_name,False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role":"assistant","content":json.dumps({"step": "observe", "output": output})})
                continue

        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break    