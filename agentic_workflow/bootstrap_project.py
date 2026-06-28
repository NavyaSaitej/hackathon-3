import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - Bootstrap Agent - %(message)s')

def run_cmd(cmd):
    try:
        logging.info(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            logging.error(f"Command failed: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        logging.error(f"Error: {e}")
        return False

def bootstrap():
    logging.info("Bootstrapping new Agentic Project Structure...")
    
    dirs = [
        "src/frontend",
        "src/backend",
        "tests",
        "docs",
        "agentic_workflow"
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        logging.info(f"Created directory: {d}")
        
    logging.info("Initializing configuration files...")
    
    # Python backend setup
    if not os.path.exists("src/backend/requirements.txt"):
        with open("src/backend/requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\npydantic\ngoogle-adk\n")
            
    # Frontend setup
    if not os.path.exists("src/frontend/package.json"):
        with open("src/frontend/package.json", "w") as f:
            f.write('{\n  "name": "frontend",\n  "version": "1.0.0"\n}\n')

    # Formatting and linting config
    if not os.path.exists("ruff.toml"):
        with open("ruff.toml", "w") as f:
            f.write('[lint]\nselect = ["E", "F", "W"]\n')

    if not os.path.exists(".prettierrc"):
        with open(".prettierrc", "w") as f:
            f.write('{\n  "semi": true,\n  "singleQuote": true\n}\n')

    # Initialize Git
    if not os.path.exists(".git"):
        run_cmd("git init")
        with open(".gitignore", "w") as f:
            f.write("venv/\nnode_modules/\n__pycache__/\n*.env\n")
        run_cmd("git add .")
        run_cmd('git commit -m "chore: initial bootstrap by agent"')

    logging.info("Bootstrap complete. Ready for development.")

if __name__ == "__main__":
    bootstrap()
