def run_job(callback, entered, release, wait_seconds=5):
    entered.set()
    if not release.wait(wait_seconds):
        raise TimeoutError("worker release timed out")
    return callback()
