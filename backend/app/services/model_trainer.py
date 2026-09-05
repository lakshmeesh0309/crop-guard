import os
import sys
import re
import asyncio
import subprocess
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

# Global training status — persisted in memory between requests
training_status = {
    "status": "idle",          # "idle" | "downloading" | "training" | "done" | "error"
    "progress": 0,             # 0-100
    "log": [],                 # list of log message strings
    "version": "v1.0",
    "accuracy": None,          # float or None
    "last_trained": None,      # ISO datetime string or None
    "dataset": "PlantVillage (Kaggle)",
    "error": None,
}

_executor = ThreadPoolExecutor(max_workers=1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
train_script = os.path.join(BASE_DIR, "ml", "train.py")

def _log(msg):
    """Append a log message to the training status."""
    training_status["log"].append(msg)
    print(f"[Trainer] {msg}")

def _run_training_sync(kaggle_username: str, kaggle_key: str):
    """Synchronous training pipeline — runs the PyTorch train.py script in a subprocess."""
    try:
        training_status["status"] = "downloading"
        training_status["progress"] = 0
        training_status["error"] = None
        training_status["accuracy"] = None
        training_status["log"] = []

        _log(f"[Setup] Starting training subprocess with python: {sys.executable}")
        _log(f"[Setup] Script path: {train_script}")

        # Start the training script as a subprocess
        cmd = [
            sys.executable, train_script,
            "--epochs", "10",
            "--kaggle-username", kaggle_username,
            "--kaggle-key", kaggle_key
        ]

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=BASE_DIR
        )

        # Read output in real-time
        for line in process.stdout:
            line_str = line.strip()
            if not line_str:
                continue

            # Intercept custom status lines
            if line_str.startswith("[TRAIN STATUS]"):
                parts = line_str.split()
                if len(parts) >= 4:
                    status_type = parts[2]
                    try:
                        progress_val = int(parts[3])
                        training_status["status"] = status_type
                        training_status["progress"] = progress_val
                    except ValueError:
                        pass
            else:
                # Log regular outputs to memory list
                _log(line_str)

                # Parse validation accuracy from final logs
                if "Best validation accuracy:" in line_str:
                    try:
                        match = re.search(r"accuracy:\s*([0-9.]+)", line_str)
                        if match:
                            training_status["accuracy"] = float(match.group(1))
                    except Exception as parse_err:
                        _log(f"[Trainer Error] Failed to parse validation accuracy: {parse_err}")

        # Wait for process to complete
        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"Training subprocess exited with non-zero code: {process.returncode}")

        # Complete status update
        training_status.update({
            "status": "done",
            "progress": 100,
            "last_trained": datetime.now(timezone.utc).isoformat(),
            "version": f"v4.{datetime.now(timezone.utc).strftime('%y%m%d')}",
        })
        _log("[Done] Training pipeline completed successfully.")

    except Exception as e:
        training_status["status"] = "error"
        training_status["error"] = str(e)
        _log(f"[ERROR] Training failed: {e}")

async def run_training(kaggle_username: str, kaggle_key: str):
    """Run training in a background thread so it doesn't block the FastAPI event loop."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        _executor, _run_training_sync, kaggle_username, kaggle_key
    )
