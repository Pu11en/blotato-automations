import sys
import tempfile
import textwrap
import threading
import time
import unittest
from pathlib import Path

from blotato.locking import LockTimeout, exclusive_lock


class ExclusiveLockTest(unittest.TestCase):
    """The lock has to work on Windows too -- the original fcntl.flock version
    could not even be imported there."""

    def test_creates_the_directory_and_lock_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "run"
            with exclusive_lock(target) as held:
                self.assertEqual(held, target)
                self.assertTrue((target / ".lock").is_file())

    def test_sequential_acquisitions_succeed(self):
        with tempfile.TemporaryDirectory() as tmp:
            for _ in range(3):
                with exclusive_lock(tmp):
                    pass

    def test_second_holder_in_another_process_times_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = textwrap.dedent(
                f"""
                import time
                from blotato.locking import exclusive_lock
                with exclusive_lock({str(Path(tmp))!r}):
                    print("held", flush=True)
                    time.sleep(5)
                """
            )
            import subprocess

            holder = subprocess.Popen(
                [sys.executable, "-c", script], stdout=subprocess.PIPE, text=True
            )
            try:
                self.assertEqual(holder.stdout.readline().strip(), "held")
                with self.assertRaises(LockTimeout):
                    with exclusive_lock(tmp, timeout=0.5, poll=0.05):
                        pass
            finally:
                holder.kill()
                holder.wait()

    def test_lock_is_released_even_when_the_body_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                with exclusive_lock(tmp):
                    raise RuntimeError("boom")
            with exclusive_lock(tmp, timeout=1):
                pass

    def test_serializes_concurrent_threads(self):
        with tempfile.TemporaryDirectory() as tmp:
            observed = []

            def worker():
                with exclusive_lock(tmp, timeout=10):
                    observed.append("enter")
                    time.sleep(0.05)
                    observed.append("exit")

            threads = [threading.Thread(target=worker) for _ in range(3)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            # Never two enters back to back: each critical section completed
            # before the next one started.
            self.assertEqual(observed, ["enter", "exit"] * 3)


if __name__ == "__main__":
    unittest.main()
