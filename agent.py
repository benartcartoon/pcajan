import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

AGENT_VERSION = "0.9.0"
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
DEFAULT_COLAB_URL = "https://colab.research.google.com/drive/1A6EpaD0g5W9_ammkd6QqxyKF5LCz2Bc9"
PROJECTS = {
    "benjapon": {"repo": "benartcartoon/benjapon", "colab_url": DEFAULT_COLAB_URL},
    "cartoonv1": {"repo": "benartcartoon/cartoonv1", "colab_url": DEFAULT_COLAB_URL},
    "cartoon": {"repo": "benartcartoon/cartoonv1", "colab_url": DEFAULT_COLAB_URL},
}

def ensure_dirs():
    for folder in (JOBS_DIR, RESULTS_DIR, LOGS_DIR): folder.mkdir(parents=True, exist_ok=True)

def log(message):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"; print(line, flush=True)
    with (LOGS_DIR / "pcajan.log").open("a", encoding="utf-8") as f: f.write(line + "\n")

def load_processed():
    if not PROCESSED_FILE.exists(): return set()
    try: return set(json.loads(PROCESSED_FILE.read_text(encoding="utf-8-sig")))
    except Exception: return set()

def save_processed(processed): PROCESSED_FILE.write_text(json.dumps(sorted(processed), indent=2), encoding="utf-8")

def rclone(*args):
    try: return subprocess.run([RCLONE, *args], capture_output=True, text=True)
    except FileNotFoundError: return subprocess.run(["rclone", *args], capture_output=True, text=True)

def archive_remote(name):
    p = rclone("moveto", f"{REMOTE_JOBS}/{name}", f"{REMOTE_STATUS}/{name}")
    if p.returncode != 0: log(f"Drive arsivleme uyarisi: {p.stderr.strip() or 'rclone hatasi'}")

def fetch_remote_jobs(processed):
    p = rclone("lsf", REMOTE_JOBS, "--include", "*.json", "--files-only")
    if p.returncode != 0: log(f"Drive jobs okunamadi: {p.stderr.strip() or 'rclone hatasi'}"); return
    for name in (x.strip() for x in p.stdout.splitlines()):
        if not name.endswith(".json"): continue
        jid = Path(name).stem
        if jid in processed: archive_remote(name); continue
        local = JOBS_DIR / name
        if not local.exists():
            c = rclone("copyto", f"{REMOTE_JOBS}/{name}", str(local))
            if c.returncode == 0: log(f"Drive'dan yeni gorev alindi: {name}")

def write_result(job_id, payload):
    target = RESULTS_DIR / f"{job_id}.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    rclone("copyto", str(target), f"{REMOTE_RESULTS}/{job_id}.json")

def chrome_windows():
    import pygetwindow as gw
    return [w for w in gw.getAllWindows() if w.title and ("Chrome" in w.title or "Colab" in w.title or "Colaboratory" in w.title)]

def activate_chrome():
    wins = chrome_windows()
    if not wins: raise RuntimeError("Chrome/Colab penceresi bulunamadi")
    win = wins[-1]
    if win.isMinimized: win.restore()
    win.activate(); time.sleep(2)
    try: win.maximize()
    except Exception: pass
    return win

def project_config(project, job):
    key = str(project or "").lower().strip(); cfg = dict(PROJECTS.get(key, {}))
    if job.get("target_url"): cfg["colab_url"] = job["target_url"]
    if job.get("repo"): cfg["repo"] = job["repo"]
    return cfg

def open_colab(url):
    os.startfile(url); wait_seconds = int(os.environ.get("COLAB_OPEN_WAIT", "18"))
    log(f"Colab aciliyor; {wait_seconds} saniye bekleniyor..."); time.sleep(wait_seconds); activate_chrome(); log("Colab acildi")

def disconnect_runtime():
    """Colab'in baglantiyi kes klavye kisayolunu kullanir; kod hucresine metin yazmaz."""
    import pyautogui
    activate_chrome()
    # Colab: Runtime > Disconnect and delete runtime dialog is exposed by Ctrl+Shift+M then menu navigation.
    # Use menu via mouse-independent keyboard: Alt+/ opens command search, search Turkish/English command.
    pyautogui.hotkey("alt", "/"); time.sleep(2)
    pyautogui.write("disconnect and delete runtime", interval=0.03); time.sleep(2)
    pyautogui.press("enter"); time.sleep(3)
    pyautogui.press("enter"); time.sleep(5)
    log("Colab runtime baglantisini kesme komutu gonderildi")

def close_colab():
    import pyautogui
    activate_chrome()
    try: disconnect_runtime()
    except Exception as exc: log(f"Runtime kapatma uyarisi: {exc}")
    activate_chrome(); pyautogui.hotkey("ctrl", "w"); time.sleep(2)
    log("Colab runtime kapatma denendi ve aktif sekme kapatildi")

def run_all_colab():
    import pyautogui
    activate_chrome(); pyautogui.hotkey("ctrl", "f9"); time.sleep(3); pyautogui.press("enter"); log("Run all (Ctrl+F9) gonderildi")

def handle_job(path, processed):
    job = json.loads(path.read_text(encoding="utf-8-sig")); job_id = str(job.get("job_id") or path.stem)
    if job_id in processed: path.unlink(missing_ok=True); return
    project = str(job.get("project", "unknown")).lower(); action = str(job.get("action", "test")).lower(); cfg = project_config(project, job)
    log(f"Gorev alindi: {job_id} | project={project} | action={action}")
    write_result(job_id,{"job_id":job_id,"status":"RUNNING","project":project,"action":action,"agent_version":AGENT_VERSION,"started_at":datetime.now().isoformat(timespec="seconds")})
    try:
        if action in {"open_colab","colab_open","open"}:
            url = cfg.get("colab_url");
            if not url: raise ValueError("Bu proje icin Colab URL tanimli degil")
            open_colab(url)
        elif action in {"close_colab","colab_close","close"}: close_colab()
        elif action in {"run","run_all","produce","generate","start_project","test"}:
            url = cfg.get("colab_url");
            if not url: raise ValueError("Bu proje icin Colab URL tanimli degil")
            log(f"Proje yonlendirildi: {project} | repo={cfg.get('repo','ozel')}"); open_colab(url); run_all_colab()
        elif action == "command":
            command = job.get("command")
            if not command: raise ValueError("command eksik")
            subprocess.Popen(command, shell=True)
        else: raise ValueError(f"Desteklenmeyen action: {action}")
        write_result(job_id,{"job_id":job_id,"status":"DONE","project":project,"action":action,"agent_version":AGENT_VERSION,"finished_at":datetime.now().isoformat(timespec="seconds")})
        processed.add(job_id); save_processed(processed); archive_remote(path.name); path.rename(path.with_suffix(".done")); log(f"Gorev tamamlandi: {job_id}")
    except Exception as exc:
        write_result(job_id,{"job_id":job_id,"status":"ERROR","error":str(exc),"agent_version":AGENT_VERSION,"failed_at":datetime.now().isoformat(timespec="seconds")})
        processed.add(job_id); save_processed(processed); archive_remote(path.name); path.rename(path.with_suffix(".error")); log(f"HATA {job_id}: {exc}")

def main():
    ensure_dirs(); processed = load_processed()
    for old in ("TEST001","TEST002","TEST003","TEST004","TEST005"): processed.add(old)
    save_processed(processed); log(f"PC AJAN basladi v{AGENT_VERSION}"); log(f"Gorev klasoru: {JOBS_DIR}")
    while True:
        try:
            fetch_remote_jobs(processed)
            for path in sorted(JOBS_DIR.glob("*.json")): handle_job(path, processed)
        except Exception as exc: log(f"Dongu hatasi: {exc}")
        time.sleep(POLL_SECONDS)

if __name__ == "__main__": main()
