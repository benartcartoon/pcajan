import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

AGENT_VERSION = "0.5.0"
POLL_SECONDS = 10
AGENT_ROOT = Path(os.environ.get("AI_AGENT_ROOT", str(Path.home() / "AI-Agent")))
JOBS_DIR = AGENT_ROOT / "jobs"
RESULTS_DIR = AGENT_ROOT / "results"
LOGS_DIR = AGENT_ROOT / "logs"
PROCESSED_FILE = AGENT_ROOT / "processed_jobs.json"
RCLONE = os.environ.get("RCLONE_EXE", r"C:\Users\berke\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.75.1-windows-amd64\rclone.exe")
REMOTE_JOBS = "gdrive:AI-Agent/jobs"
REMOTE_STATUS = "gdrive:AI-Agent/status"
REMOTE_RESULTS = "gdrive:AI-Agent/results"


def ensure_dirs():
    for folder in (JOBS_DIR, RESULTS_DIR, LOGS_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def log(message):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (LOGS_DIR / "pcajan.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_processed():
    if not PROCESSED_FILE.exists():
        return set()
    try:
        return set(json.loads(PROCESSED_FILE.read_text(encoding="utf-8-sig")))
    except Exception:
        return set()


def save_processed(processed):
    PROCESSED_FILE.write_text(json.dumps(sorted(processed), indent=2), encoding="utf-8")


def rclone(*args):
    try:
        p = subprocess.run([RCLONE, *args], capture_output=True, text=True)
    except FileNotFoundError:
        p = subprocess.run(["rclone", *args], capture_output=True, text=True)
    return p


def archive_remote(name):
    p = rclone("moveto", f"{REMOTE_JOBS}/{name}", f"{REMOTE_STATUS}/{name}")
    if p.returncode != 0:
        log(f"Drive arsivleme uyarisi: {p.stderr.strip() or 'rclone hatasi'}")


def fetch_remote_jobs(processed):
    p = rclone("lsf", REMOTE_JOBS, "--include", "*.json", "--files-only")
    if p.returncode != 0:
        log(f"Drive jobs okunamadi: {p.stderr.strip() or 'rclone hatasi'}")
        return
    for name in (x.strip() for x in p.stdout.splitlines()):
        if not name.endswith(".json"):
            continue
        job_id = Path(name).stem
        if job_id in processed:
            archive_remote(name)
            continue
        local = JOBS_DIR / name
        if not local.exists():
            c = rclone("copyto", f"{REMOTE_JOBS}/{name}", str(local))
            if c.returncode == 0:
                log(f"Drive'dan yeni gorev alindi: {name}")
            else:
                log(f"Gorev indirilemedi: {name}")


def write_result(job_id, payload):
    target = RESULTS_DIR / f"{job_id}.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rclone("copyto", str(target), f"{REMOTE_RESULTS}/{job_id}.json")


def activate_chrome():
    import pygetwindow as gw
    windows = [w for w in gw.getAllWindows() if w.title and ("Colab" in w.title or "Chrome" in w.title)]
    if not windows:
        raise RuntimeError("Chrome/Colab penceresi bulunamadi")
    win = windows[-1]
    if win.isMinimized:
        win.restore()
    win.activate()
    time.sleep(2)
    try:
        win.maximize()
    except Exception:
        pass
    time.sleep(1)


def run_all_colab():
    import pyautogui
    activate_chrome()
    width, height = pyautogui.size()
    pyautogui.click(int(width * 0.55), int(height * 0.45))
    time.sleep(1)
    pyautogui.hotkey("ctrl", "f9")
    log("Colab odaklandi ve Run all (Ctrl+F9) gonderildi")
    time.sleep(3)
    pyautogui.press("enter")


def launch_colab(url):
    os.startfile(url)
    wait_seconds = int(os.environ.get("COLAB_OPEN_WAIT", "18"))
    log(f"Colab aciliyor; {wait_seconds} saniye bekleniyor...")
    time.sleep(wait_seconds)
    import pyautogui  # noqa: F401
    import pygetwindow  # noqa: F401
    run_all_colab()


def handle_job(path, processed):
    job = json.loads(path.read_text(encoding="utf-8-sig"))
    job_id = str(job.get("job_id") or path.stem)
    if job_id in processed:
        path.unlink(missing_ok=True)
        return
    project = job.get("project", "unknown")
    repo = job.get("repo", "")
    runner = job.get("runner", "colab")
    action = job.get("action", "test")
    target_url = job.get("target_url")
    log(f"Gorev alindi: {job_id} | project={project} | action={action}")
    write_result(job_id, {"job_id": job_id, "status": "RUNNING", "project": project, "repo": repo, "runner": runner, "action": action, "agent_version": AGENT_VERSION, "started_at": datetime.now().isoformat(timespec="seconds")})
    try:
        if runner == "colab":
            if not target_url:
                raise ValueError("Colab gorevi icin target_url eksik")
            launch_colab(target_url)
        elif runner == "command":
            command = job.get("command")
            if not command:
                raise ValueError("command runner icin command eksik")
            subprocess.Popen(command, shell=True)
        else:
            raise ValueError(f"Desteklenmeyen runner: {runner}")
        write_result(job_id, {"job_id": job_id, "status": "LAUNCHED", "project": project, "repo": repo, "runner": runner, "action": action, "agent_version": AGENT_VERSION, "launched_at": datetime.now().isoformat(timespec="seconds")})
        processed.add(job_id)
        save_processed(processed)
        archive_remote(path.name)
        path.rename(path.with_suffix(".done"))
        log(f"Gorev baslatildi: {job_id}")
    except Exception as exc:
        write_result(job_id, {"job_id": job_id, "status": "ERROR", "error": str(exc), "agent_version": AGENT_VERSION, "failed_at": datetime.now().isoformat(timespec="seconds")})
        processed.add(job_id)
        save_processed(processed)
        archive_remote(path.name)
        path.rename(path.with_suffix(".error"))
        log(f"HATA {job_id}: {exc}")


def main():
    ensure_dirs()
    processed = load_processed()
    for old in ("TEST001", "TEST002", "TEST003", "TEST004"):
        processed.add(old)
    save_processed(processed)
    log(f"PC AJAN basladi v{AGENT_VERSION}")
    log(f"Gorev klasoru: {JOBS_DIR}")
    while True:
        try:
            fetch_remote_jobs(processed)
            for path in sorted(JOBS_DIR.glob("*.json")):
                handle_job(path, processed)
        except Exception as exc:
            log(f"Dongu hatasi: {exc}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
