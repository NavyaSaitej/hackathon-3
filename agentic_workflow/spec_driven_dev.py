import os
import subprocess
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - SDD Subagent - %(message)s')

def spec_driven_validation():
    logging.info("Starting Spec-Driven Development Validation...")
    
    # Check if a spec file exists
    spec_path = ".speckit/templates/specify.md"
    if not os.path.exists(spec_path):
        logging.warning(f"Spec file not found at {spec_path}. SDD validation skipped.")
        return
        
    logging.info(f"Loaded specification from {spec_path}. Validating...")
    
    # Here, a real SDD agent would parse the spec and run targeted unit tests
    # For this generalized framework, we'll run Pytest (if available) as the validation step.
    
    if os.path.exists("tests/"):
        logging.info("Running test suite against specifications...")
        result = subprocess.run(r"python -m pytest tests/", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info("All specifications met. Tests passed.")
        else:
            logging.error(f"Spec validation failed:\n{result.stdout}\n{result.stderr}")
    else:
        logging.warning("No tests/ directory found. Cannot validate specs against code.")

if __name__ == "__main__":
    spec_driven_validation()
