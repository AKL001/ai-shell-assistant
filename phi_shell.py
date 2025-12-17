#!/home/akl001/bin/phiAi/venv/bin/python3
import ollama
import sys
import os
import subprocess

# 1. Initialize the Client
client = ollama.Client()
MODEL = "phi3:mini"

# 2. Security Blocklist (The "Safety Gear")
BLOCKLIST = ["rm -rf /", "mkfs", "> /dev/sda", "dd if=", ":(){ :|:& };:"]

def get_ai_command(user_query):
    try:
        # Use Chat API for better instruction following
        response = client.chat(
            model=MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a Linux Expert. Output ONLY the raw command. No chat, no backticks, no markdown labels like "bash" or "shell".'
                },
                {
                    'role': 'user',
                    'content': f'Command for: {user_query}'
                }
            ],
            options={
                'temperature': 0,  # Zero randomness for technical accuracy
                'stop': ['\n', '```', 'Assistant:'] # Cut off rambling immediately
            }
        )
        
        # Clean the output
        raw_content = response['message']['content'].strip()
        # Remove common "hallucinated" labels
        clean_cmd = raw_content.replace('bash', '').replace('shell', '').replace('`', '').strip()
        return clean_cmd
        
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"

def main():
    # Handle input from CLI args or interactive prompt
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Phi-3 AI Assist > ")
    
    if not query: return

    print("\033[94m[Thinking...]\033[0m")
    cmd = get_ai_command(query)

    if any(b in cmd for b in BLOCKLIST):
        print(f"\n\033[91m[SECURITY ALERT]\033[0m Command blocked: {cmd}")
        return

    print(f"\nProposed: \033[1;32m{cmd}\033[0m")
    print("--------------------------------")
    print("[1] Execute  [2] Copy  [3] Cancel")
    
    # --- THE FIX ---
    # We open the terminal device (/dev/tty) directly to avoid the Zsh crash
    try:
        with open('/dev/tty', 'r') as tty:
            print("\nAction (1/2/3): ", end='', flush=True)
            choice = tty.readline().strip()
    except Exception:
        # Fallback if /dev/tty isn't available
        choice = input("\nAction (1/2/3): ")

    if choice == '1':
        print("\033[93mExecuting...\033[0m")
        os.system(cmd)
    elif choice == '2':
        clipboard = "pbcopy" if os.uname().sysname == 'Darwin' else "xclip -selection clipboard"
        subprocess.run(clipboard.split(), input=cmd.encode())
        print("✓ Copied.")
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
