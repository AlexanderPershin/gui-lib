import subprocess
import threading


class OSCommandRunner:
    def __init__(self, on_output_callback):
        self.callback = on_output_callback

    def run(self, command: str):
        thread = threading.Thread(
            target=self._execute, args=(command,), daemon=True
        )
        thread.start()

    def _execute(self, command: str):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            output = result.stdout
            if result.stderr:
                output += result.stderr
            self.callback(output.strip() or "(no output)")
        except subprocess.TimeoutExpired:
            self.callback("Too long time to execute...")
        except Exception as e:
            self.callback(f"Error: {e}")
