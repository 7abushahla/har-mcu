#!/usr/bin/env python3
"""Local reproducibility setup for the HAR MCU experiments.

This helper downloads the WISDM and Arduino activity-recognition archives when
needed, normalizes WISDM into the repository's expected CSV layout, and can run
optional checks for the main replication notebook plus WISDM, Arduino, and v2
augmentation M3 experiment entrypoints. The validation paths keep the same
GPU-first behavior as the corresponding notebook and M3 runtime policy when a
GPU is visible. It never submits Slurm jobs.
"""

from __future__ import annotations

import argparse
import copy
import csv
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable


EXPECTED_WISDM_ROWS = 1_098_207
MIN_WISDM_ROWS = 1_000_000
WISDM_COLUMNS = ["user", "activity", "timestamp", "x-axis", "y-axis", "z-axis"]
WISDM_CLASSES = {"Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"}
EXPECTED_ARDUINO_ROWS = 240_620
MIN_ARDUINO_ROWS = 200_000
ARDUINO_CSV_NAME = "Arduino_layth_hamza_wisdm_raw_numeric_user.csv"

DEFAULT_GOOGLE_DRIVE_ID = "1r2MUejp-x4-JxCvDB552GJKn3LdhiJXM"
DEFAULT_ARDUINO_GOOGLE_DRIVE_ID = "1G2J5-QqWzTmXbReGxUW7aKugFXK0FZlF"
DEFAULT_OFFICIAL_PAGE = "https://www.cis.fordham.edu/wisdm/dataset.php"
DEFAULT_OFFICIAL_ARCHIVES = (
    "https://www.cis.fordham.edu/wisdm/includes/datasets/latest/WISDM_ar_latest.tar.gz",
)


def log(message: str) -> None:
    print(f"[setup] {message}", flush=True)


def repo_root_default() -> Path:
    return Path(__file__).resolve().parents[1]


def run_command(cmd: list[str], *, cwd: Path) -> None:
    log("running: " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd), check=True)


def import_requests():
    try:
        import requests  # type: ignore
    except ImportError:
        return None
    return requests


def archive_kind(path: Path) -> str | None:
    if zipfile.is_zipfile(path):
        return "zip"
    if tarfile.is_tarfile(path):
        return "tar"
    return None


def ensure_safe_child(base: Path, target: Path) -> None:
    base_resolved = base.resolve()
    target_resolved = target.resolve()
    try:
        target_resolved.relative_to(base_resolved)
    except ValueError as exc:
        raise RuntimeError(f"Archive member escapes extraction directory: {target}") from exc


def extract_archive(archive_path: Path, wisdm_dir: Path, cache_dir: Path) -> None:
    kind = archive_kind(archive_path)
    if kind is None:
        raise RuntimeError(f"Downloaded file is not a zip or tar archive: {archive_path}")

    cache_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wisdm_extract_", dir=str(cache_dir)) as tmp_name:
        tmp_dir = Path(tmp_name)
        log(f"extracting {archive_path.name}")
        if kind == "zip":
            with zipfile.ZipFile(archive_path) as zf:
                for member in zf.infolist():
                    ensure_safe_child(tmp_dir, tmp_dir / member.filename)
                zf.extractall(tmp_dir)
        else:
            with tarfile.open(archive_path) as tf:
                for member in tf.getmembers():
                    ensure_safe_child(tmp_dir, tmp_dir / member.name)
                tf.extractall(tmp_dir)

        raw_txt_matches = list(tmp_dir.rglob("WISDM_ar_v1.1_raw.txt"))
        if not raw_txt_matches:
            raise RuntimeError("Archive did not contain WISDM_ar_v1.1_raw.txt")

        source_dir = raw_txt_matches[0].parent
        if wisdm_dir.exists():
            log(f"using existing directory {wisdm_dir}")
        else:
            wisdm_dir.mkdir(parents=True, exist_ok=True)

        for source in source_dir.iterdir():
            if source.is_file() and (
                source.name.startswith("WISDM_ar_v1.1") or source.name == "readme.txt"
            ):
                shutil.copy2(source, wisdm_dir / source.name)


def extract_arduino_archive(
    archive_path: Path,
    arduino_dir: Path,
    cache_dir: Path,
    *,
    csv_name: str,
) -> None:
    kind = archive_kind(archive_path)
    if kind is None:
        raise RuntimeError(f"Downloaded file is not a zip or tar archive: {archive_path}")

    cache_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="arduino_extract_", dir=str(cache_dir)) as tmp_name:
        tmp_dir = Path(tmp_name)
        log(f"extracting {archive_path.name}")
        if kind == "zip":
            with zipfile.ZipFile(archive_path) as zf:
                for member in zf.infolist():
                    ensure_safe_child(tmp_dir, tmp_dir / member.filename)
                zf.extractall(tmp_dir)
        else:
            with tarfile.open(archive_path) as tf:
                for member in tf.getmembers():
                    ensure_safe_child(tmp_dir, tmp_dir / member.name)
                tf.extractall(tmp_dir)

        csv_matches = list(tmp_dir.rglob(csv_name))
        if not csv_matches:
            raise RuntimeError(f"Archive did not contain {csv_name}")

        arduino_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(csv_matches[0], arduino_dir / csv_name)


def write_response_to_file(response, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)


def google_confirm_token(response) -> str | None:
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    content_type = response.headers.get("content-type", "").lower()
    if "text/html" not in content_type and "text/plain" not in content_type:
        return None
    match = re.search(r"confirm=([0-9A-Za-z_]+)", response.text[:100_000])
    return match.group(1) if match else None


def download_google_drive(file_id: str, output_path: Path) -> None:
    requests = import_requests()
    if requests is None:
        raise RuntimeError(
            "Google Drive downloads require the requests package. "
            "Run the setup wrapper so requirements.txt is installed first."
        )

    session = requests.Session()
    base_url = "https://drive.google.com/uc?export=download"
    response = session.get(base_url, params={"id": file_id}, stream=True, timeout=60)
    response.raise_for_status()
    token = google_confirm_token(response)
    if token:
        response = session.get(
            base_url,
            params={"id": file_id, "confirm": token},
            stream=True,
            timeout=60,
        )
        response.raise_for_status()
    write_response_to_file(response, output_path)


def download_url(url: str, output_path: Path) -> None:
    requests = import_requests()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if requests is not None:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        write_response_to_file(response, output_path)
        return

    with urllib.request.urlopen(url, timeout=60) as response, output_path.open("wb") as f:
        shutil.copyfileobj(response, f)


def fetch_text(url: str) -> str:
    requests = import_requests()
    if requests is not None:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response.text
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def discover_official_archives(page_url: str) -> list[str]:
    try:
        html = fetch_text(page_url)
    except Exception as exc:
        log(f"official page discovery failed: {exc}")
        return []

    urls: list[str] = []
    for href in re.findall(r"href=[\"']([^\"']+)[\"']", html, flags=re.IGNORECASE):
        if "WISDM_ar" not in href:
            continue
        if not re.search(r"\.(zip|tar\.gz|tgz)(?:$|\?)", href, flags=re.IGNORECASE):
            continue
        urls.append(urllib.parse.urljoin(page_url, href))
    return urls


def candidate_downloads(args: argparse.Namespace) -> list[tuple[str, str, str]]:
    candidates: list[tuple[str, str, str]] = []
    for url in args.download_url:
        name = Path(urllib.parse.urlparse(url).path).name or "WISDM_ar_v1.1.archive"
        candidates.append(("url", url, name))
    if not args.no_google_drive:
        candidates.append(("google", args.google_drive_file_id, "WISDM_ar_v1.1.zip"))
    if not args.no_official:
        official_urls = list(DEFAULT_OFFICIAL_ARCHIVES)
        official_urls.extend(discover_official_archives(args.official_page_url))
        seen: set[str] = set()
        for url in official_urls:
            if url in seen:
                continue
            seen.add(url)
            name = Path(urllib.parse.urlparse(url).path).name or "WISDM_ar_latest.tar.gz"
            candidates.append(("url", url, name))
    return candidates


def download_wisdm_archive(args: argparse.Namespace, cache_dir: Path) -> Path:
    errors: list[str] = []
    for kind, value, filename in candidate_downloads(args):
        archive_path = cache_dir / filename
        if archive_path.exists() and archive_kind(archive_path) and not args.force_download:
            log(f"using cached archive {archive_path}")
            return archive_path

        log(f"downloading WISDM archive via {kind}: {value}")
        try:
            if archive_path.exists():
                archive_path.unlink()
            if kind == "google":
                download_google_drive(value, archive_path)
            else:
                download_url(value, archive_path)
            if archive_kind(archive_path) is None:
                archive_path.unlink(missing_ok=True)
                raise RuntimeError("downloaded file was not a valid archive")
            return archive_path
        except Exception as exc:
            errors.append(f"{kind}:{value}: {exc}")
            log(f"download candidate failed: {exc}")

    raise RuntimeError("All WISDM download candidates failed:\n- " + "\n- ".join(errors))


def arduino_candidate_downloads(args: argparse.Namespace) -> list[tuple[str, str, str]]:
    candidates: list[tuple[str, str, str]] = []
    for url in args.arduino_download_url:
        name = Path(urllib.parse.urlparse(url).path).name or "tiny-motion.zip"
        candidates.append(("url", url, name))
    if not args.no_arduino_google_drive:
        candidates.append(("google", args.arduino_google_drive_file_id, "tiny-motion.zip"))
    return candidates


def download_arduino_archive(args: argparse.Namespace, cache_dir: Path) -> Path:
    errors: list[str] = []
    for kind, value, filename in arduino_candidate_downloads(args):
        archive_path = cache_dir / filename
        if archive_path.exists() and archive_kind(archive_path) and not args.force_arduino_download:
            log(f"using cached archive {archive_path}")
            return archive_path

        log(f"downloading Arduino archive via {kind}: {value}")
        try:
            if archive_path.exists():
                archive_path.unlink()
            if kind == "google":
                download_google_drive(value, archive_path)
            else:
                download_url(value, archive_path)
            if archive_kind(archive_path) is None:
                archive_path.unlink(missing_ok=True)
                raise RuntimeError("downloaded file was not a valid archive")
            return archive_path
        except Exception as exc:
            errors.append(f"{kind}:{value}: {exc}")
            log(f"download candidate failed: {exc}")

    raise RuntimeError("All Arduino download candidates failed:\n- " + "\n- ".join(errors))


def convert_wisdm_txt_to_csv(wisdm_dir: Path, *, force: bool = False) -> Path:
    raw_txt = wisdm_dir / "WISDM_ar_v1.1_raw.txt"
    raw_csv = wisdm_dir / "WISDM_ar_v1.1_raw.csv"
    if raw_csv.exists() and not force:
        return raw_csv
    if not raw_txt.exists():
        raise FileNotFoundError(f"Missing WISDM raw text file: {raw_txt}")

    log("converting WISDM_ar_v1.1_raw.txt to WISDM_ar_v1.1_raw.csv")
    rows = 0
    bad_rows = 0
    with raw_csv.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.writer(dst)
        writer.writerow(WISDM_COLUMNS)
        for record in iter_wisdm_raw_records(raw_txt):
            try:
                parts = next(csv.reader([record]))
            except csv.Error:
                bad_rows += 1
                continue
            parts = [part.strip() for part in parts]
            while parts and parts[-1] == "":
                parts.pop()
            if len(parts) != 6:
                bad_rows += 1
                continue
            writer.writerow(parts)
            rows += 1
    if rows < MIN_WISDM_ROWS:
        raise RuntimeError(f"Converted only {rows} WISDM rows; expected about {EXPECTED_WISDM_ROWS}")
    if bad_rows:
        log(f"conversion skipped {bad_rows} malformed rows")
    return raw_csv


def iter_wisdm_raw_records(raw_txt: Path) -> Iterable[str]:
    """Yield semicolon-terminated WISDM raw records.

    The official text dump is mostly one record per line, but a few records are
    concatenated and a later block uses a trailing comma before the semicolon.
    Splitting on the actual record terminator keeps those rows recoverable.
    """

    buffer = ""
    with raw_txt.open("r", encoding="utf-8", errors="replace", newline="") as src:
        while True:
            chunk = src.read(1024 * 1024)
            if not chunk:
                break
            buffer += chunk.replace("\x00", "")
            while ";" in buffer:
                record, buffer = buffer.split(";", 1)
                record = record.strip()
                if record:
                    yield record
        tail = buffer.strip()
        if tail:
            yield tail


def validate_wisdm_csv(raw_csv: Path, *, strict: bool = False) -> dict[str, object]:
    if not raw_csv.exists():
        raise FileNotFoundError(f"Missing WISDM CSV: {raw_csv}")

    activity_counts: Counter[str] = Counter()
    users: set[str] = set()
    rows = 0
    with raw_csv.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        missing = [col for col in WISDM_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise RuntimeError(f"WISDM CSV missing required columns: {missing}")
        for row in reader:
            rows += 1
            users.add(str(row["user"]))
            activity_counts[str(row["activity"])] += 1

    missing_classes = sorted(WISDM_CLASSES - set(activity_counts))
    if rows < MIN_WISDM_ROWS:
        raise RuntimeError(f"WISDM CSV has {rows} rows, expected at least {MIN_WISDM_ROWS}")
    if strict and rows != EXPECTED_WISDM_ROWS:
        raise RuntimeError(f"WISDM CSV has {rows} rows, expected exactly {EXPECTED_WISDM_ROWS}")
    if missing_classes:
        raise RuntimeError(f"WISDM CSV missing activity classes: {missing_classes}")

    log(f"WISDM CSV ok: rows={rows}, users={len(users)}, classes={len(activity_counts)}")
    return {
        "rows": rows,
        "users": len(users),
        "activity_counts": dict(activity_counts),
        "csv": str(raw_csv),
    }


def validate_arduino_csv(raw_csv: Path, *, strict: bool = False) -> dict[str, object]:
    if not raw_csv.exists():
        raise FileNotFoundError(f"Missing Arduino CSV: {raw_csv}")

    activity_counts: Counter[str] = Counter()
    users: set[str] = set()
    rows = 0
    empty_cells = 0
    bad_numeric = 0
    with raw_csv.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        missing = [col for col in WISDM_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise RuntimeError(f"Arduino CSV missing required columns: {missing}")
        for row in reader:
            rows += 1
            values = {col: str(row.get(col, "")).strip() for col in WISDM_COLUMNS}
            empty_cells += sum(1 for value in values.values() if value == "")
            users.add(values["user"])
            activity_counts[values["activity"]] += 1
            for col in ("timestamp", "x-axis", "y-axis", "z-axis"):
                try:
                    float(values[col])
                except ValueError:
                    bad_numeric += 1

    missing_classes = sorted(WISDM_CLASSES - set(activity_counts))
    if rows < MIN_ARDUINO_ROWS:
        raise RuntimeError(f"Arduino CSV has {rows} rows, expected at least {MIN_ARDUINO_ROWS}")
    if strict and rows != EXPECTED_ARDUINO_ROWS:
        raise RuntimeError(
            f"Arduino CSV has {rows} rows, expected exactly {EXPECTED_ARDUINO_ROWS}"
        )
    if missing_classes:
        raise RuntimeError(f"Arduino CSV missing activity classes: {missing_classes}")
    if empty_cells:
        raise RuntimeError(f"Arduino CSV has {empty_cells} empty required cells")
    if bad_numeric:
        raise RuntimeError(f"Arduino CSV has {bad_numeric} non-numeric timestamp/axis cells")
    if strict and len(users) != 2:
        raise RuntimeError(f"Arduino CSV has {len(users)} users, expected exactly 2")

    log(f"Arduino CSV ok: rows={rows}, users={len(users)}, classes={len(activity_counts)}")
    return {
        "rows": rows,
        "users": len(users),
        "activity_counts": dict(activity_counts),
        "csv": str(raw_csv),
    }


def normalize_wisdm_csv(wisdm_dir: Path, *, strict: bool = False, force: bool = False) -> Path:
    raw_csv = wisdm_dir / "WISDM_ar_v1.1_raw.csv"
    raw_txt = wisdm_dir / "WISDM_ar_v1.1_raw.txt"

    if force or not raw_csv.exists():
        raw_csv = convert_wisdm_txt_to_csv(wisdm_dir, force=True)

    summary = validate_wisdm_csv(raw_csv, strict=False)
    if int(summary["rows"]) != EXPECTED_WISDM_ROWS and raw_txt.exists():
        log(
            "existing CSV row count differs from the WISDM release; "
            "regenerating CSV from WISDM_ar_v1.1_raw.txt"
        )
        raw_csv = convert_wisdm_txt_to_csv(wisdm_dir, force=True)
        summary = validate_wisdm_csv(raw_csv, strict=False)

    if strict and int(summary["rows"]) != EXPECTED_WISDM_ROWS:
        raise RuntimeError(
            f"WISDM CSV has {summary['rows']} rows, expected exactly {EXPECTED_WISDM_ROWS}"
        )
    return raw_csv


def ensure_wisdm(args: argparse.Namespace, repo_root: Path) -> Path:
    wisdm_dir = repo_root / args.wisdm_dir
    cache_dir = repo_root / args.cache_dir
    raw_csv = wisdm_dir / "WISDM_ar_v1.1_raw.csv"

    if raw_csv.exists() and not args.force_download:
        log(f"found existing {raw_csv}")
        return normalize_wisdm_csv(
            wisdm_dir,
            strict=args.strict_data,
            force=args.force_convert_csv,
        )

    archive_path: Path | None = None
    if args.archive:
        archive_path = Path(args.archive)
        if not archive_path.is_absolute():
            archive_path = repo_root / archive_path
        if not archive_path.exists():
            raise FileNotFoundError(f"Archive not found: {archive_path}")
    elif not args.skip_download:
        archive_path = download_wisdm_archive(args, cache_dir)

    if archive_path is not None:
        extract_archive(archive_path, wisdm_dir, cache_dir)
    elif not wisdm_dir.exists():
        raise FileNotFoundError(
            f"{wisdm_dir} does not exist and downloads were skipped. "
            "Provide --archive or remove --skip-download."
        )

    return normalize_wisdm_csv(
        wisdm_dir,
        strict=args.strict_data,
        force=args.force_convert_csv,
    )


def ensure_arduino(args: argparse.Namespace, repo_root: Path) -> Path | None:
    if args.skip_arduino:
        log("Arduino data setup skipped")
        return None

    arduino_dir = repo_root / args.arduino_dir
    raw_csv = arduino_dir / args.arduino_csv
    cache_dir = repo_root / args.cache_dir

    if raw_csv.exists() and not args.force_arduino_download:
        log(f"found existing {raw_csv}")
        validate_arduino_csv(raw_csv, strict=args.strict_data)
        return raw_csv

    archive_path: Path | None = None
    if args.arduino_archive:
        archive_path = Path(args.arduino_archive)
        if not archive_path.is_absolute():
            archive_path = repo_root / archive_path
        if not archive_path.exists():
            raise FileNotFoundError(f"Arduino archive not found: {archive_path}")
    elif not args.skip_download and not args.skip_arduino_download:
        archive_path = download_arduino_archive(args, cache_dir)

    if archive_path is not None:
        extract_arduino_archive(
            archive_path,
            arduino_dir,
            cache_dir,
            csv_name=args.arduino_csv,
        )
    elif not raw_csv.exists():
        raise FileNotFoundError(
            f"{raw_csv} does not exist and Arduino downloads were skipped. "
            "Provide --arduino-archive or remove --skip-download/--skip-arduino-download."
        )

    validate_arduino_csv(raw_csv, strict=args.strict_data)
    return raw_csv


def patch_notebook_for_setup(nb) -> None:
    replacements = {
        'RUN_MODE = "full"': 'RUN_MODE = "quick"',
        'PROTOCOLS = ["random_stratified", "user_holdout"]': 'PROTOCOLS = ["random_stratified"]',
        "RUN_QAT = True": "RUN_QAT = False",
        "AUTHOR_STYLE_REP_SAMPLES = 100": "AUTHOR_STYLE_REP_SAMPLES = 8",
        "FAIL_FAST = False": "FAIL_FAST = True",
        'cfg["smoke"]["max_windows_per_class"] = 200': 'cfg["smoke"]["max_windows_per_class"] = 20',
        "epochs=50,": "epochs=1,",
        "V2_REP_SAMPLES = 100": "V2_REP_SAMPLES = 8",
    }
    for cell in nb.cells:
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        for old, new in replacements.items():
            source = source.replace(old, new)
        cell["source"] = source
        cell["outputs"] = []
        cell["execution_count"] = None


def truncate_notebook_for_smoke(nb) -> None:
    last_idx = None
    for idx, cell in enumerate(nb.cells):
        source = cell.get("source", "")
        if "raw_df, sanity = load_wisdm_dataframe" in source:
            last_idx = idx
            break
    if last_idx is None:
        raise RuntimeError("Could not find WISDM data-loading cell in replication notebook")
    nb.cells = nb.cells[: last_idx + 1]


def validate_notebook(args: argparse.Namespace, repo_root: Path) -> None:
    if args.notebook_check == "skip":
        log("notebook validation skipped")
        return
    try:
        import nbformat  # type: ignore
        from nbclient import NotebookClient  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Notebook validation requires nbformat and nbclient. "
            "Run scripts/setup_repro.sh so requirements.txt is installed."
        ) from exc

    notebook_path = repo_root / args.notebook
    if not notebook_path.exists():
        raise FileNotFoundError(f"Notebook not found: {notebook_path}")

    nb = nbformat.read(notebook_path, as_version=4)
    nb = copy.deepcopy(nb)
    patch_notebook_for_setup(nb)
    if args.notebook_check == "smoke":
        truncate_notebook_for_smoke(nb)

    out_dir = repo_root / "notebooks" / "executed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"setup_{args.notebook_check}_{notebook_path.name}"
    client = NotebookClient(
        nb,
        timeout=args.notebook_timeout,
        kernel_name=args.kernel_name,
        resources={"metadata": {"path": str(repo_root)}},
    )
    try:
        client.execute()
    finally:
        nbformat.write(nb, out_path)
    log(f"notebook {args.notebook_check} validation ok: {out_path}")


def validate_m3_command(
    args: argparse.Namespace,
    repo_root: Path,
    *,
    check: str,
    config: str,
    model_variant: str,
    artifact_suffix: str,
    label: str,
    augmentation_args: list[str] | None = None,
) -> None:
    if check == "skip":
        log(f"{label} validation skipped")
        return
    if check == "smoke" and args.m3_max_windows_per_class < 4:
        raise RuntimeError(
            "--m3-max-windows-per-class must be at least 4 for the six-class "
            "random-stratified smoke split"
        )

    if augmentation_args is None:
        augmentation_args = ["--disable-accel-rotation"]

    cmd = [
        sys.executable,
        "-m",
        "src.m3.run_experiment",
        "--config",
        config,
        "--smoke",
        "--model-variant",
        model_variant,
        "--artifact-suffix",
        artifact_suffix,
        "--max-windows-per-class",
        str(args.m3_max_windows_per_class),
        "--representative-samples",
        str(args.m3_representative_samples),
        "--timing-warmup-samples",
        "1",
        "--timing-timed-samples",
        "2",
        *augmentation_args,
    ]
    if check == "dry-run":
        cmd.append("--dry-run")
    if not args.m3_enable_qat:
        cmd.append("--disable-qat")
    run_command(cmd, cwd=repo_root)
    log(f"{label} {check} validation ok")


def validate_m3(args: argparse.Namespace, repo_root: Path) -> None:
    validate_m3_command(
        args,
        repo_root,
        check=args.m3_check,
        config=args.m3_config,
        model_variant=args.m3_model_variant,
        artifact_suffix=args.m3_artifact_suffix,
        label="M3 WISDM",
    )


def validate_arduino_m3(args: argparse.Namespace, repo_root: Path) -> None:
    if args.skip_arduino:
        log("M3 Arduino validation skipped because Arduino data setup was skipped")
        return
    check = args.arduino_m3_check or args.m3_check
    validate_m3_command(
        args,
        repo_root,
        check=check,
        config=args.arduino_m3_config,
        model_variant=args.arduino_m3_model_variant or args.m3_model_variant,
        artifact_suffix=args.arduino_m3_artifact_suffix or args.m3_artifact_suffix,
        label="M3 Arduino",
    )


def validate_v2_augmentation_core(args: argparse.Namespace) -> None:
    import numpy as np

    from src.train.augment import accel_rotation_settings, rotate_normalized_accel_windows

    cfg = {
        "augment": {
            "accel_rotation": {
                "enabled": True,
                "probability": 1.0,
                "apply_in_qat": True,
                "mode": "bounded_so3",
                "max_angle_degrees": args.v2_augment_max_angle_degrees,
            }
        }
    }
    settings = accel_rotation_settings(cfg)
    X = np.asarray(
        [
            [[0.0, 0.0, 1.0], [0.1, 0.0, 0.98], [0.2, 0.0, 0.96], [0.1, 0.1, 0.98]],
            [[0.0, 1.0, 0.0], [0.0, 0.9, 0.1], [0.0, 0.8, 0.2], [0.1, 0.8, 0.2]],
            [[1.0, 0.0, 0.0], [0.9, 0.1, 0.0], [0.8, 0.2, 0.0], [0.8, 0.2, 0.1]],
            [[0.4, 0.4, 0.8], [0.5, 0.3, 0.8], [0.4, 0.5, 0.7], [0.3, 0.5, 0.8]],
        ],
        dtype=np.float32,
    )
    mean = np.zeros(3, dtype=np.float32)
    std = np.ones(3, dtype=np.float32)
    augmented = rotate_normalized_accel_windows(
        X,
        mean=mean,
        std=std,
        settings=settings,
        rng=np.random.default_rng(2026),
    )
    if augmented.shape != X.shape:
        raise RuntimeError(f"v2 augmentation changed shape from {X.shape} to {augmented.shape}")
    if not np.isfinite(augmented).all():
        raise RuntimeError("v2 augmentation produced non-finite values")
    if np.allclose(augmented, X):
        raise RuntimeError("v2 augmentation self-test did not rotate the synthetic windows")
    before_norm = np.linalg.norm(X, axis=-1)
    after_norm = np.linalg.norm(augmented, axis=-1)
    if not np.allclose(before_norm, after_norm, rtol=1e-4, atol=1e-4):
        raise RuntimeError("v2 augmentation did not preserve per-sample acceleration norms")
    log(
        "v2 augmentation core check ok: mode=bounded_so3, "
        f"max_angle_degrees={args.v2_augment_max_angle_degrees:g}, "
        f"integration_probability={args.v2_augment_probability:g}"
    )


def validate_v2_augmentation(args: argparse.Namespace, repo_root: Path) -> None:
    if args.v2_augment_check == "skip":
        log("M3 v2 augmentation validation skipped")
        return
    if not 0.0 < args.v2_augment_probability <= 1.0:
        raise RuntimeError("--v2-augment-probability must be in (0, 1]")
    if args.skip_arduino and "arduino" in args.v2_augment_config.lower():
        raise RuntimeError(
            "--v2-augment-check with the default Arduino config requires Arduino data. "
            "Remove --skip-arduino or pass a WISDM-only --v2-augment-config."
        )

    validate_v2_augmentation_core(args)
    validate_m3_command(
        args,
        repo_root,
        check=args.v2_augment_check,
        config=args.v2_augment_config,
        model_variant=args.v2_augment_model_variant or args.m3_model_variant,
        artifact_suffix=args.v2_augment_artifact_suffix,
        label="M3 v2 augmentation",
        augmentation_args=[
            "--enable-accel-rotation",
            "--accel-rotation-mode",
            "bounded_so3",
            "--accel-rotation-probability",
            str(args.v2_augment_probability),
            "--accel-rotation-max-angle-degrees",
            str(args.v2_augment_max_angle_degrees),
        ],
    )


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=repo_root_default())
    parser.add_argument("--wisdm-dir", default="WISDM_ar_v1.1")
    parser.add_argument("--cache-dir", default="data/raw_cache")
    parser.add_argument("--archive", default=None, help="Use a local WISDM zip/tar archive")
    parser.add_argument("--download-url", action="append", default=[], help="Additional archive URL")
    parser.add_argument("--google-drive-file-id", default=DEFAULT_GOOGLE_DRIVE_ID)
    parser.add_argument("--official-page-url", default=DEFAULT_OFFICIAL_PAGE)
    parser.add_argument("--no-google-drive", action="store_true")
    parser.add_argument("--no-official", action="store_true")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--force-download", action="store_true")
    parser.add_argument("--force-convert-csv", action="store_true")
    parser.add_argument("--strict-data", action="store_true")

    parser.add_argument("--skip-arduino", action="store_true")
    parser.add_argument("--arduino-dir", default="tiny-motion")
    parser.add_argument("--arduino-csv", default=ARDUINO_CSV_NAME)
    parser.add_argument("--arduino-archive", default=None, help="Use a local tiny-motion zip/tar archive")
    parser.add_argument("--arduino-download-url", action="append", default=[], help="Additional Arduino archive URL")
    parser.add_argument("--arduino-google-drive-file-id", default=DEFAULT_ARDUINO_GOOGLE_DRIVE_ID)
    parser.add_argument("--no-arduino-google-drive", action="store_true")
    parser.add_argument("--skip-arduino-download", action="store_true")
    parser.add_argument("--force-arduino-download", action="store_true")

    parser.add_argument(
        "--notebook-check",
        choices=["skip", "smoke", "execute"],
        default="skip",
        help=(
            "Default skip. smoke executes notebook preflight/data cells only; "
            "execute runs the patched quick-mode notebook end to end."
        ),
    )
    parser.add_argument("--notebook", default="notebooks/replication_deepconvlstm.ipynb")
    parser.add_argument("--notebook-timeout", type=int, default=1800)
    parser.add_argument("--kernel-name", default="python3")

    parser.add_argument("--m3-check", choices=["skip", "dry-run", "smoke"], default="skip")
    parser.add_argument("--m3-config", default="configs/m3/E00_wisdm_m2_anchor.yaml")
    parser.add_argument("--m3-model-variant", default="daghero_cnn_2layer_conv2d")
    parser.add_argument("--m3-artifact-suffix", default="setup_smoke/{model_variant}/{experiment_code}")
    parser.add_argument("--m3-max-windows-per-class", type=int, default=8)
    parser.add_argument("--m3-representative-samples", type=int, default=4)
    parser.add_argument("--m3-enable-qat", action="store_true")
    parser.add_argument(
        "--arduino-m3-check",
        choices=["skip", "dry-run", "smoke"],
        default=None,
        help="Arduino M3 validation mode; default follows --m3-check.",
    )
    parser.add_argument("--arduino-m3-config", default="configs/m3/E10_arduino_from_scratch.yaml")
    parser.add_argument("--arduino-m3-model-variant", default=None)
    parser.add_argument("--arduino-m3-artifact-suffix", default=None)
    parser.add_argument(
        "--v2-augment-check",
        choices=["skip", "dry-run", "smoke"],
        default="skip",
        help=(
            "Validate the v2 bounded accelerometer-rotation path. dry-run checks "
            "config/CLI wiring; smoke also runs a tiny M3 training/eval/export pass."
        ),
    )
    parser.add_argument("--v2-augment-config", default="configs/m3/E10_arduino_from_scratch.yaml")
    parser.add_argument("--v2-augment-model-variant", default=None)
    parser.add_argument(
        "--v2-augment-artifact-suffix",
        default="setup_smoke/v2_augment_bounded20_p025/{model_variant}/{experiment_code}",
    )
    parser.add_argument("--v2-augment-probability", type=float, default=0.25)
    parser.add_argument("--v2-augment-max-angle-degrees", type=float, default=20.0)
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = args.repo_root.resolve()
    os.chdir(repo_root)
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    raw_csv = ensure_wisdm(args, repo_root)
    log(f"WISDM ready: {raw_csv.relative_to(repo_root)}")
    arduino_csv = ensure_arduino(args, repo_root)
    if arduino_csv is not None:
        log(f"Arduino data ready: {arduino_csv.relative_to(repo_root)}")
    validate_notebook(args, repo_root)
    validate_m3(args, repo_root)
    validate_arduino_m3(args, repo_root)
    validate_v2_augmentation(args, repo_root)
    log("local reproducibility setup complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
