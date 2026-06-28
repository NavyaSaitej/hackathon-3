import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - QA Subagent - %(message)s')

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def continuous_qa():
    logging.info("Starting Agentic Continuous QA Loop...")
    while True:
        try:
            # Format and Lint Python
            logging.info("Running Python format & lint (Ruff)...")
            run_cmd(r"python -m ruff format src/backend/")
            run_cmd(r"python -m ruff check src/backend/ --fix")
            
            # Format JS/CSS
            logging.info("Running Prettier (Frontend)...")
            run_cmd(r"npx prettier --write src/frontend/**/*.{js,css,html}")
            
            # Check Git status for automatic local commits
            success, stdout, stderr = run_cmd("git status --porcelain")
            if stdout.strip():
                logging.info("Detected code changes. Creating local checkpoint commit...")
                run_cmd("git add src/")
                run_cmd('git commit -m "Auto-Agent: QA format & lint checkpoint"')
                logging.info("Local checkpoint committed successfully.")
            
        except Exception as e:
            logging.error(f"QA Loop Error: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    continuous_qa()
