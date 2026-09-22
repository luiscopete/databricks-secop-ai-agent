#!/usr/bin/env python3
"""Start AgentServer locally and verify health + one agent request."""

import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def wait_for_health(base_url: str, process: subprocess.Popen, timeout: int = 60) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(f"{base_url}/health", timeout=2) as response:
                payload = json.loads(response.read())
                if payload.get("status") == "healthy":
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False


def stop_process(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        else:
            process.terminate()
        process.wait(timeout=10)
    except Exception:
        process.kill()


def main() -> None:
    port = find_free_port()
    base_url = f"http://127.0.0.1:{port}"

    popen_kwargs = {
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "text": True,
    }
    if os.name == "posix":
        popen_kwargs["preexec_fn"] = os.setsid

    process = subprocess.Popen(
        ["uv", "run", "start-server", "--port", str(port)],
        **popen_kwargs,
    )

    try:
        print(f"1. Starting AgentServer on {base_url} ...")
        if not wait_for_health(base_url, process):
            print("FAILED: AgentServer did not become healthy.")
            if process.stdout:
                print(process.stdout.read())
            sys.exit(1)
        print("   OK")

        print("2. Sending a test request ...")
        body = json.dumps(
            {
                "input": [
                    {
                        "role": "user",
                        "content": "Say hello in one short sentence.",
                    }
                ]
            }
        ).encode("utf-8")

        request = urllib.request.Request(
            f"{base_url}/invocations",
            data=body,
            headers={"Content-Type": "application/json"},
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read())

        if not result.get("output"):
            print("FAILED: /invocations returned no output.")
            print(result)
            sys.exit(1)

        print("   OK")
        print("Preflight passed.")

    finally:
        stop_process(process)


if __name__ == "__main__":
    main()
