import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - DevOps Subagent - %(message)s')

def run_cmd(cmd):
    try:
        logging.info(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def devops_security_scan():
    logging.info("Starting DevOps & Security Scan...")
    
    # 1. Security Check (Bandit)
    logging.info("Running AST-based security analysis (Bandit)...")
    success, stdout, stderr = run_cmd(r"python -m bandit -r src/backend/")
    if success:
        logging.info("Security scan passed. No critical vulnerabilities found.")
    else:
        logging.warning(f"Security vulnerabilities detected:\n{stdout}")

    # 2. Deadcode Check (Vulture)
    logging.info("Running deadcode analysis (Vulture)...")
    success, stdout, stderr = run_cmd(r"python -m vulture src/backend/")
    if success:
        logging.info("Deadcode scan passed. Codebase is clean.")
    else:
        logging.warning(f"Deadcode detected (requires review):\n{stdout}")
        
    logging.info("DevOps & Security Scan complete.")

if __name__ == "__main__":
    devops_security_scan()
