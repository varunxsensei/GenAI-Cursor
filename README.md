# 🧠 GenAI-Cursor
## _An AI-Powered Terminal Assistant using OpenAI GPT-4o_

GenAI-Cursor is a smart command-line assistant built in Python that uses OpenAI’s GPT-4o with function-calling. It interprets natural language into real terminal commands and executes them. It follows a structured reasoning loop: Plan → Action → Observe → Output.

---

## 🖥️ Demo
<video width="640" height="360" controls>
  <source src="video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## ✨ Features

- 🧠 Understands natural language input
- 🖥️ Executes real shell commands
- 📁 Create, delete, and manage files
- 📜 Tracks command history and file changes
- 🔄 Structured loop: Plan → Action → Observe → Output
- 🧩 Easily extendable with new tools
- 💻 Cross-platform (Windows, macOS, Linux)

---

## 📁 Project Structure

```
genai-cursor/
├── main.py              # Main CLI logic and OpenAI integration
├── .env.example         # Template for environment variables
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/varunxsensei/genai-cursor.git
cd genai-cursor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

Copy the example env file:

```bash
cp .env.example .env
```

Then add your key to `.env`:

```
OPENAI_API_KEY=your_api_key_here
```

---

## ⚙️ Usage

Start the assistant with:

```bash
python main.py
```

Example commands:

```text
> create a file called test.py
> delete test.py
> show command history
> quit
```

---

## 🔧 Tools Available

| Tool          | Description                            |
|---------------|----------------------------------------|
| run_command   | Executes shell commands via os.system  |

🧩 You can extend tools with:
- `read_file(filename)`
- `write_file(filename, content)`
- `list_files()`
- `search_stackoverflow(query)`

---

## 🧪 Example Interaction

```bash
> create a file called hello.py
🧠: Planning step executed...
🤖: File 'hello.py' created.

> delete hello.py
🧠: Planning step executed...
🤖: File 'hello.py' deleted.

> what files have I created?
🤖: Files created: ['hello.py']

> quit
```

---

## 📦 Dependencies

- Python 3.10+
- openai
- python-dotenv

Install manually:

```bash
pip install openai python-dotenv
```

---

## 🧠 Prompt Engineering Logic

Each command follows a loop:

1. `plan` – Understand the user intent.
2. `action` – Call an available tool (like `run_command`).
3. `observe` – See the result of the action.
4. `output` – Return the final response to the user.

This enables intelligent, step-by-step reasoning via LLM.

---

## 🧩 Future Ideas

- ✅ Track created/deleted files
- ✅ Maintain session command history
- ⌨️ Add read/write file support
- 🌐 Search documentation/Stack Overflow via LLM
- 🐳 Docker support
- 🧪 Add test framework and CLI args

---

## 🤝 Contributing

Pull requests are welcome!  
Fork the repository, make your changes, and open a PR.

---

## 🪪 License

MIT License  
**Free Software, Hell Yeah!**

---

> Built with 💻, 🔥, and GPT-4o — by a coder, for coders.
