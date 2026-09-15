import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

AGENT_VERSION = "0.4.0"
POLL_SECONDS = 10
AGENT_ROOT = Path(os.environ.get("AI_AGENT_ROOT", str(Path.home() / "AI-Agent")))
JOBS_DIR = AGENT_ROOT / "jobs"
RESULTS_DIR = AGENT_ROOT / "results"
LOGS_DIR = AGENT_ROOT / "logs"


def ensure_dirs():
    for folder in (JOBS_DIR, RESULTS_DIR, LOGS_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def log(message):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    print(line, flush=True)
    with (LOGS_DIR / "pcajan.log").open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def write_result(job_id, payload):
    target = RESULTS_DIR / f"{job_id}.json"
    temp = target.with_suffix(".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(target)


def activate_chrome():
    import pygetwindow as gw
    windows = [w for w in gw.getAllWindows() if w.title and ("Colab" in w.title or "Chrome" in w.title)]
    if not windows:
        raise RuntimeError("Chrome/Colab penceresi bulunamadi")
    win = windows[-1]
    try:
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(2)
        try:
            win.maximize()
        except Exception:
            pass
        time.sleep(1)
    except Exception as exc:
        raise RuntimeError(f"Chrome penceresi odaklanamadi: {exc}") from exc
    return win


def run_all_colab():
    import pyautogui
    activate_chrome()

    # Once notebook alanina tiklayip Colab'a klavye odagi ver.
    width, height = pyautogui.size()
    pyautogui.click(int(width * 0.55), int(height * 0.45))
    time.sleep(1)

    # Colab'in resmi Run all kisayolu. Onceki surumde sorun tarayici odagiydi;
    # v0.4 Chrome'u acikca one getirip notebook'a odak verdikten sonra yollar.
    pyautogui.hotkey("ctrl", "f9")
    log("Colab odaklandi ve Run all (Ctrl+F9) gonderildi")
    time.sleep(3)

    # Olası guven/onay penceresinde varsayilan secimi kabul et.
    pyautogui.press("enter")


def launch_colab(url):
    os.startfile(url)
    wait_seconds = int(os.environ.get("COLAB_OPEN_WAIT", "18"))
    log(f"Colab aciliyor; {wait_seconds} saniye bekleniyor...")
    time.sleep(wait_seconds)
    try:
        import pyautogui  # noqa: F401
        import pygetwindow  # noqa: F401
    except ImportError as exc:
        raise RuntimeError("pyautogui/pygetwindow kurulu degil. install.bat calistir.") from exc
    run_all_colab()


def handle_job(path):
    job = json.loads(path.read_text(encoding="utf-8-sig"))
    job_id = str(job.get("job_id") or path.stem)
    project = job.get("project", "unknown")
    repo = job.get("repo", "")
    runner = job.get("runner", "colab")
    action = job.get("action", "test")
    target_url = job.get("target_url")

    log(f"Gorev alindi: {job_id} | project={project} | action={action}")
    write_result(job_id, {
        "job_id": job_id, "status": "RUNNING", "project": project,
        "repo": repo, "runner": runner, "action": action,
        "agent_version": AGENT_VERSION,
        "started_at": datetime.now().isoformat(timespec="seconds")
    })

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

        write_result(job_id, {
            "job_id": job_id, "status": "LAUNCHED", "project": project,
            "repo": repo, "runner": runner, "action": action,
            "agent_version": AGENT_VERSION,
            "launched_at": datetime.now().isoformat(timespec="seconds")
        })
        path.rename(path.with_suffix(".done"))
        log(f"Gorev baslatildi: {job_id}")
    except Exception as exc:
        write_result(job_id, {
            "job_id": job_id, "status": "ERROR", "error": str(exc),
            "agent_version": AGENT_VERSION,
            "failed_at": datetime.now().isoformat(timespec="seconds")
        })
        path.rename(path.with_suffix(".error"))
        log(f"HATA {job_id}: {exc}")


def main():
    ensure_dirs()
    log(f"PC AJAN basladi v{AGENT_VERSION}")
    log(f"Gorev klasoru: {JOBS_DIR}")
    while True:
        try:
            for path in sorted(JOBS_DIR.glob("*.json")):
                handle_job(path)
        except Exception as exc:
            log(f"Dongu hatasi: {exc}")
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
