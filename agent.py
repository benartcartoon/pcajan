import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

AGENT_VERSION = "0.2.0"
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


def launch_colab(url):
    # Chrome'u ac, Colab sayfasini bekle, sonra Colab'in Run all kisayolunu gonder.
    # pyautogui yalnizca klavye tusunu yollar; sifre veya Google kimlik bilgisi okumaz.
    os.startfile(url)
    wait_seconds = int(os.environ.get("COLAB_OPEN_WAIT", "12"))
    log(f"Colab aciliyor; {wait_seconds} saniye bekleniyor...")
    time.sleep(wait_seconds)
    try:
        import pyautogui
    except ImportError as exc:
        raise RuntimeError("pyautogui kurulu degil. Repo klasorunde install.bat calistir.") from exc
    pyautogui.hotkey("ctrl", "f9")
    log("Colab Run all (Ctrl+F9) gonderildi")


def handle_job(path):
    job = json.loads(path.read_text(encoding="utf-8"))
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
