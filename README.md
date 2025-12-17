# ShellGuard AI 🛡️

> A Secure, Local-First AI Terminal Copilot powered by Microsoft Phi-3 & Ollama

ShellGuard AI is a lightweight Python tool that allows you to generate and execute Linux commands using natural language. It runs entirely on your local machine for maximum privacy and features a safety-first architecture.

---

## 🛠️ Requirements

- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: ~2.5GB (for the Phi-3:mini model)
- **Ollama**: Must be installed and running ([Install Ollama](https://ollama.ai))
- **Python**: 3.10+ installed

---

## 🚀 Installation

### 1. Automated Setup (`install.sh`)

The repository includes an `install.sh` script that automates the setup of the environment, model, and shortcuts.

To install ShellGuard AI, run the following commands:

```bash
chmod +x install.sh
./install.sh
```

This will automatically:
- Create the necessary directories
- Set up a Python virtual environment
- Install the Ollama library
- Pull the Phi-3:mini model
- Create a global `phi` command
- Configure the `Ctrl + K` keyboard shortcut for Zsh

### 2. Manual Configuration

If you prefer manual setup:

1. **Project Path**: `~/bin/phiAI/phi_shell.py`
2. **Venv Path**: `~/bin/phiAI/venv`
3. **Shebang**: Ensure the first line of your Python script uses the absolute path to your venv:

```python
#!/home/YOUR_USER/bin/phiAI/venv/bin/python3
```

4. Install dependencies:

```bash
~/bin/phiAI/venv/bin/pip install ollama
```

5. Pull the model:

```bash
ollama pull phi3:mini
```

---

## 🔒 Security Features

Unlike standard AI wrappers, ShellGuard AI uses a **Deterministic Safety Layer**:

1. **Python Blocklist**: Hardcoded filter prevents execution of dangerous commands like `rm -rf /`, `mkfs`, etc.
2. **Chat-Based Grounding**: Uses the `ollama.chat` API with a System Role to prevent hallucinations like the "bash" prefix
3. **Human-in-the-Loop**: Every command must be confirmed via an interactive menu before running

---

## ⌨️ Usage

### Via Command Line

```bash
phi "how do I find large files"
```

### Via Keyboard Shortcut

Press `Ctrl + K`, type your request in the minibuffer, and hit Enter.

### Interactive Menu

Once a command is proposed, you can choose:

1. **Execute**: Runs the command immediately
2. **Copy**: Sends the command to your clipboard
3. **Cancel**: Aborts the operation

---

## 🧠 Technical Logic

- **Temperature 0**: Ensures technical accuracy and repeatable results
- **TTY Handling**: Uses `/dev/tty` for input to allow the menu to function correctly even when called from a shell widget
- **Stop Tokens**: Configured to cut off the AI the moment the command is finished to prevent rambling

---

## 🐛 Troubleshooting

### Zsh Widget Not Loading

If the `Ctrl + K` shortcut doesn't work after installation:

1. **Reload your shell configuration**:
   ```bash
   source ~/.zshrc
   ```

2. **Verify the widget is registered**:
   ```bash
   zle -la | grep phi_widget
   ```
   You should see `phi_widget` in the output.

3. **Check for conflicts**:
   ```bash
   bindkey | grep '\^K'
   ```
   If another command is bound to `Ctrl + K`, you may need to unbind it first or choose a different key.

4. **Test the widget manually**:
   ```bash
   phi_widget
   ```

### Ollama Connection Issues

If you see connection errors:

1. **Verify Ollama is running**:
   ```bash
   ollama list
   ```

2. **Start Ollama service**:
   ```bash
   ollama serve
   ```

3. **Check model availability**:
   ```bash
   ollama list | grep phi3
   ```

### Permission Denied

If you get permission errors when running `phi`:

```bash
chmod +x ~/bin/phiAI/phi_shell.py
chmod +x ~/bin/phi
```

---

## 📝 Example Queries

- `"Find all files larger than 100MB"`
- `"Show me disk usage by directory"`
- `"List all running Docker containers"`
- `"Search for Python files modified in the last 7 days"`
- `"Create a backup of my home directory"`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## ⚠️ Disclaimer

Always review commands before executing them. While ShellGuard AI includes safety features, you remain responsible for what runs on your system.