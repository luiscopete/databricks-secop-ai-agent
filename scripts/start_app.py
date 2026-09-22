#!/usr/bin/env python3
"""Start the SECOP AI backend and the Databricks reference chat frontend."""

import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "e2e-chatbot-app-next"
TEMP_REPO_DIR = ROOT / ".tmp-app-templates"


def ensure_frontend() -> None:
    """Fetch only the Databricks reference chatbot frontend when it is absent."""
    if FRONTEND_DIR.exists():
        return

    print("Reference chat UI not found. Fetching e2e-chatbot-app-next...")
    shutil.rmtree(TEMP_REPO_DIR, ignore_errors=True)

    subprocess.run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            "https://github.com/databricks/app-templates.git",
            str(TEMP_REPO_DIR),
        ],
        check=True,
    )
    subprocess.run(
        ["git", "sparse-checkout", "set", "e2e-chatbot-app-next"],
        cwd=TEMP_REPO_DIR,
        check=True,
    )

    shutil.move(
        str(TEMP_REPO_DIR / "e2e-chatbot-app-next"),
        str(FRONTEND_DIR),
    )
    shutil.rmtree(TEMP_REPO_DIR, ignore_errors=True)


def terminate(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()


def main() -> None:
    load_dotenv(ROOT / ".env", override=True)

    backend_port = 8000
    frontend_port = os.getenv("CHAT_APP_PORT", os.getenv("PORT", "3000"))

    # The frontend proxies chat requests to MLflow AgentServer.
    os.environ["API_PROXY"] = os.getenv(
        "API_PROXY",
        f"http://localhost:{backend_port}/invocations",
    )
    os.environ["CHAT_APP_PORT"] = frontend_port

    ensure_frontend()

    print("Installing/building chat UI...")
    subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    backend = None
    frontend = None

    try:
        backend = subprocess.Popen(
            ["uv", "run", "start-server", "--host", "0.0.0.0", "--port", str(backend_port)],
            cwd=ROOT,
        )

        # Give AgentServer a brief opportunity to bind before starting the UI.
        time.sleep(2)
        if backend.poll() is not None:
            raise RuntimeError("AgentServer exited during startup")

        frontend = subprocess.Popen(
            ["npm", "run", "start"],
            cwd=FRONTEND_DIR,
            env=os.environ.copy(),
        )

        while True:
            if backend.poll() is not None:
                raise RuntimeError(f"AgentServer exited with code {backend.returncode}")
            if frontend.poll() is not None:
                raise RuntimeError(f"Chat UI exited with code {frontend.returncode}")
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        terminate(frontend)
        terminate(backend)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    main()
