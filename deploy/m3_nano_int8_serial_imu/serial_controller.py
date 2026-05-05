#!/usr/bin/env python3
"""
HAR Nano Serial Desktop Controller
===================================
Connects to the Arduino Nano 33 BLE running m3_nano_int8_serial_imu.ino over
USB Serial and lets you Start/Stop recording and trigger the long-hold average
— all from a desktop UI, without a physical shield button.

Same UX as the BLE version, but uses pyserial (USB cable) instead of bleak (BLE).

Requirements:
    pip install pyserial

Usage:
    python serial_controller.py
    python serial_controller.py --port /dev/cu.usbmodem1433401
    python serial_controller.py --baud 115200

Serial protocol (matches the .ino):
    Commands sent (line-terminated):
        start | stop | toggle   → toggle recording
        avg                     → average buffered trials
        gt <name>               → set ground truth (Walking, Jogging, ...)
        ping                    → request a [PONG]+[STATE] reply

    Lines parsed from the firmware:
        [STATE] recording=0|1            → updates state badge / button label
        [PONG] m3_nano_int8_serial_imu   → heartbeat reply (connection OK)
        trial=N win=k/M ... pred=NAME conf=X.X%   → updates live prediction
"""
from __future__ import annotations

import argparse
import queue
import re
import threading
import time
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

import serial
import serial.tools.list_ports

# ── Constants ────────────────────────────────────────────────────────────────
DEFAULT_BAUD = 115200
CLASS_NAMES = ["Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"]
PRED_RE  = re.compile(r"\bpred=([A-Za-z]+)\b.*?conf=([0-9.]+)\s*%")
STATE_RE = re.compile(r"\[STATE\]\s+recording=(\d)")

# ── Colour palette (matches ble_controller.py) ───────────────────────────────
CLR_BG       = "#1e1e2e"
CLR_SURFACE  = "#2a2a3e"
CLR_ACCENT   = "#89b4fa"
CLR_GREEN    = "#a6e3a1"
CLR_RED      = "#f38ba8"
CLR_YELLOW   = "#f9e2af"
CLR_TEXT     = "#cdd6f4"
CLR_MUTED    = "#6c7086"
CLR_START    = "#a6e3a1"
CLR_STOP     = "#f38ba8"
CLR_AVG      = "#fab387"


# ── Serial worker thread ─────────────────────────────────────────────────────
class SerialWorker:
    """Owns the pyserial port; communicates with the GUI through queues."""

    def __init__(
        self,
        port: str,
        baud: int,
        to_gui: queue.Queue,
        from_gui: queue.Queue,
    ) -> None:
        self._port = port
        self._baud = baud
        self._to_gui = to_gui
        self._from_gui = from_gui
        self._stop = threading.Event()
        self._ser: serial.Serial | None = None

    # ── public: called from GUI thread ──
    def send_cmd(self, cmd: str) -> None:
        # Always include both \n and \r so any line-ending mode on the firmware works.
        self._from_gui.put_nowait(cmd.strip() + "\n")

    def stop(self) -> None:
        self._stop.set()

    # ── thread body ──
    def _notify(self, msg: dict) -> None:
        self._to_gui.put_nowait(msg)

    def run(self) -> None:
        try:
            self._notify({"type": "log", "msg": f"Opening {self._port} @ {self._baud}…"})
            self._ser = serial.Serial(self._port, self._baud, timeout=0.1)
            # Many Arduino sketches reset on DTR toggle, so we expect ~2 s of silence after open.
            time.sleep(0.2)
            self._notify({"type": "connected", "port": self._port})
            # Ask firmware for current state.
            self._ser.write(b"ping\n")
            self._ser.flush()
        except Exception as exc:
            self._notify({"type": "error", "msg": f"Open failed: {exc}"})
            self._notify({"type": "disconnected"})
            return

        line_buf = bytearray()
        try:
            while not self._stop.is_set():
                # ── Drain GUI → firmware command queue ──
                try:
                    while True:
                        cmd = self._from_gui.get_nowait()
                        self._ser.write(cmd.encode("utf-8", errors="ignore"))
                        self._ser.flush()
                except queue.Empty:
                    pass

                # ── Read firmware → GUI lines (non-blocking) ──
                try:
                    chunk = self._ser.read(256)
                except Exception as exc:
                    self._notify({"type": "error", "msg": f"Read failed: {exc}"})
                    break
                if chunk:
                    line_buf.extend(chunk)
                    while True:
                        nl = line_buf.find(b"\n")
                        if nl < 0:
                            break
                        raw = bytes(line_buf[:nl]).rstrip(b"\r")
                        del line_buf[: nl + 1]
                        try:
                            line = raw.decode("utf-8", errors="replace").rstrip()
                        except Exception:
                            continue
                        if line:
                            self._handle_line(line)
                else:
                    time.sleep(0.02)
        finally:
            try:
                if self._ser is not None and self._ser.is_open:
                    self._ser.close()
            except Exception:
                pass
            self._notify({"type": "disconnected"})

    def _handle_line(self, line: str) -> None:
        # Always pass the raw line to the log.
        self._notify({"type": "log", "msg": line})

        m = STATE_RE.search(line)
        if m is not None:
            self._notify({"type": "state", "recording": m.group(1) == "1"})
            return

        m = PRED_RE.search(line)
        if m is not None:
            label = m.group(1)
            conf = float(m.group(2))
            # Map firmware short names ("Sit") to UI class names ("Sitting") if needed.
            for canonical in CLASS_NAMES:
                if canonical.lower().startswith(label.lower()):
                    label = canonical
                    break
            self._notify({"type": "pred", "label": label, "conf": conf})
            return


# ── Tkinter GUI ──────────────────────────────────────────────────────────────
class App(tk.Tk):
    POLL_MS = 50

    def __init__(self, port: str | None, baud: int) -> None:
        super().__init__()
        self.title("HAR Nano Serial Controller")
        self.configure(bg=CLR_BG)
        self.resizable(False, False)

        self._baud = baud
        self._port_var = tk.StringVar(value=port or "")
        self._gt_var = tk.StringVar(value="(none)")
        self._to_gui:   queue.Queue = queue.Queue()
        self._from_gui: queue.Queue = queue.Queue()
        self._worker:   SerialWorker | None = None
        self._worker_thread: threading.Thread | None = None
        self._connected = False
        self._recording = False

        self._build_ui()
        self._refresh_ports(initial=True)
        if port:
            self._connect()
        self._poll()

    # ── UI construction ──────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        title_f = tkfont.Font(family="Helvetica", size=16, weight="bold")
        tk.Label(self, text="HAR Nano Serial", font=title_f,
                 bg=CLR_BG, fg=CLR_ACCENT).pack(pady=(18, 2))
        tk.Label(self, text="m3_nano_int8_serial_imu",
                 bg=CLR_BG, fg=CLR_MUTED, font=("Helvetica", 9)).pack()

        # Port chooser
        port_frame = tk.Frame(self, bg=CLR_SURFACE)
        port_frame.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(port_frame, text="Port:", bg=CLR_SURFACE, fg=CLR_MUTED,
                 font=("Helvetica", 9)).grid(row=0, column=0, padx=(8, 4), pady=8)
        self._port_menu = tk.OptionMenu(port_frame, self._port_var, "")
        self._port_menu.config(bg=CLR_BG, fg=CLR_TEXT, activebackground=CLR_SURFACE,
                                activeforeground=CLR_ACCENT, relief="flat",
                                highlightthickness=0, font=("Courier", 10), width=22)
        self._port_menu["menu"].config(bg=CLR_BG, fg=CLR_TEXT,
                                        activebackground=CLR_SURFACE,
                                        activeforeground=CLR_ACCENT)
        self._port_menu.grid(row=0, column=1, padx=(0, 4), pady=8, sticky="w")
        tk.Button(port_frame, text="↻", command=lambda: self._refresh_ports(),
                  bg=CLR_SURFACE, fg=CLR_TEXT, activebackground=CLR_BG,
                  relief="flat", bd=0, cursor="hand2", width=2,
                  font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=2, pady=8)
        self._btn_connect = tk.Button(
            port_frame, text="Connect", command=self._toggle_connect,
            bg=CLR_ACCENT, fg="#1e1e2e", relief="flat", bd=0, cursor="hand2",
            font=("Helvetica", 10, "bold"), padx=10, pady=4,
        )
        self._btn_connect.grid(row=0, column=3, padx=(6, 8), pady=8)

        # Status bar
        status_frame = tk.Frame(self, bg=CLR_SURFACE)
        status_frame.pack(fill="x", padx=16, pady=(4, 4))
        tk.Label(status_frame, text="Serial:", bg=CLR_SURFACE, fg=CLR_MUTED,
                 font=("Helvetica", 9)).grid(row=0, column=0, padx=(8, 2), pady=6)
        self._lbl_link = tk.Label(status_frame, text="disconnected", bg=CLR_SURFACE,
                                   fg=CLR_RED, font=("Helvetica", 9, "bold"))
        self._lbl_link.grid(row=0, column=1, padx=(0, 16), pady=6, sticky="w")
        tk.Label(status_frame, text="State:", bg=CLR_SURFACE, fg=CLR_MUTED,
                 font=("Helvetica", 9)).grid(row=0, column=2, padx=(8, 2), pady=6)
        self._lbl_state = tk.Label(status_frame, text="idle", bg=CLR_SURFACE,
                                    fg=CLR_MUTED, font=("Helvetica", 9, "bold"))
        self._lbl_state.grid(row=0, column=3, padx=(0, 16), pady=6, sticky="w")

        # Prediction display
        pred_frame = tk.Frame(self, bg=CLR_SURFACE)
        pred_frame.pack(fill="x", padx=16, pady=4)
        tk.Label(pred_frame, text="Last prediction", bg=CLR_SURFACE, fg=CLR_MUTED,
                 font=("Helvetica", 9)).pack(pady=(8, 2))
        pred_f = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self._lbl_pred = tk.Label(pred_frame, text="—", font=pred_f,
                                   bg=CLR_SURFACE, fg=CLR_TEXT, width=12)
        self._lbl_pred.pack()
        self._lbl_conf = tk.Label(pred_frame, text="", bg=CLR_SURFACE, fg=CLR_MUTED,
                                   font=("Helvetica", 10))
        self._lbl_conf.pack(pady=(0, 10))

        # Buttons
        btn_frame = tk.Frame(self, bg=CLR_BG)
        btn_frame.pack(padx=16, pady=10)
        btn_style = {"font": ("Helvetica", 13, "bold"), "relief": "flat",
                     "bd": 0, "cursor": "hand2", "width": 10, "pady": 10}
        self._btn_start = tk.Button(
            btn_frame, text="▶  START", bg=CLR_START, fg="#1e1e2e",
            command=self._on_toggle, **btn_style,
        )
        self._btn_start.grid(row=0, column=0, padx=6, pady=4)
        self._btn_avg = tk.Button(
            btn_frame, text="⊞  AVERAGE", bg=CLR_AVG, fg="#1e1e2e",
            command=self._on_average, **btn_style,
        )
        self._btn_avg.grid(row=0, column=1, padx=6, pady=4)

        # Ground truth selector
        gt_frame = tk.Frame(self, bg=CLR_SURFACE)
        gt_frame.pack(fill="x", padx=16, pady=(0, 4))
        tk.Label(gt_frame, text="Ground truth (sent on selection):",
                 bg=CLR_SURFACE, fg=CLR_MUTED, font=("Helvetica", 9)).pack(
                     anchor="w", padx=10, pady=(8, 2))
        gt_inner = tk.Frame(gt_frame, bg=CLR_SURFACE)
        gt_inner.pack(padx=6, pady=(0, 8))
        opts = ["(none)"] + CLASS_NAMES
        for i, name in enumerate(opts):
            tk.Radiobutton(
                gt_inner, text=name, variable=self._gt_var, value=name,
                command=self._on_gt_changed,
                bg=CLR_SURFACE, fg=CLR_TEXT, selectcolor=CLR_BG,
                activebackground=CLR_SURFACE, activeforeground=CLR_ACCENT,
                font=("Helvetica", 10),
            ).grid(row=i // 4, column=i % 4, sticky="w", padx=6, pady=2)

        # Log box
        log_frame = tk.Frame(self, bg=CLR_BG)
        log_frame.pack(fill="both", padx=16, pady=(4, 16))
        tk.Label(log_frame, text="Log", bg=CLR_BG, fg=CLR_MUTED,
                 font=("Helvetica", 9)).pack(anchor="w")
        self._log = tk.Text(log_frame, height=8, bg=CLR_SURFACE, fg=CLR_TEXT,
                             font=("Courier", 9), relief="flat",
                             state="disabled", wrap="word")
        self._log.pack(fill="both")

        self._set_buttons_enabled(False)

    # ── Port handling ────────────────────────────────────────────────────────
    def _refresh_ports(self, initial: bool = False) -> None:
        ports = sorted(p.device for p in serial.tools.list_ports.comports())
        # Heuristic: Arduino on macOS typically appears as /dev/cu.usbmodem*.
        likely = [p for p in ports if "usbmodem" in p or "usbserial" in p
                  or p.startswith(("COM", "/dev/ttyACM", "/dev/ttyUSB"))]
        ordered = likely + [p for p in ports if p not in likely]
        if not ordered:
            ordered = ["(no ports found)"]

        menu = self._port_menu["menu"]
        menu.delete(0, "end")
        for p in ordered:
            menu.add_command(label=p, command=lambda v=p: self._port_var.set(v))
        if initial and not self._port_var.get():
            self._port_var.set(ordered[0])

    # ── Connect / disconnect ─────────────────────────────────────────────────
    def _toggle_connect(self) -> None:
        if self._connected:
            self._disconnect()
        else:
            self._connect()

    def _connect(self) -> None:
        port = self._port_var.get().strip()
        if not port or "no ports" in port:
            messagebox.showwarning("No port", "Pick a serial port first.")
            return
        self._worker = SerialWorker(port, self._baud, self._to_gui, self._from_gui)
        self._worker_thread = threading.Thread(target=self._worker.run, daemon=True)
        self._worker_thread.start()

    def _disconnect(self) -> None:
        if self._worker is not None:
            self._worker.stop()

    # ── Button handlers ──────────────────────────────────────────────────────
    def _on_toggle(self) -> None:
        if self._worker is None:
            return
        # Optimistic local flip — firmware will confirm via [STATE].
        self._worker.send_cmd("toggle")

    def _on_average(self) -> None:
        if self._worker is None:
            return
        self._worker.send_cmd("avg")
        self._log_msg("[GUI] Average (long-hold) requested")

    def _on_gt_changed(self) -> None:
        if self._worker is None:
            return
        v = self._gt_var.get()
        if v == "(none)" or not v:
            return
        self._worker.send_cmd(f"gt {v}")

    # ── State helpers ────────────────────────────────────────────────────────
    def _set_buttons_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self._btn_start.config(state=state)
        self._btn_avg.config(state=state)

    def _update_record_ui(self) -> None:
        if self._recording:
            self._btn_start.config(text="■  STOP", bg=CLR_STOP)
            self._lbl_state.config(text="recording", fg=CLR_RED)
        else:
            self._btn_start.config(text="▶  START", bg=CLR_START)
            self._lbl_state.config(text="idle", fg=CLR_MUTED)

    def _log_msg(self, msg: str) -> None:
        self._log.config(state="normal")
        self._log.insert("end", msg + "\n")
        self._log.see("end")
        self._log.config(state="disabled")

    # ── Event-queue polling on the tkinter main loop ─────────────────────────
    def _poll(self) -> None:
        while True:
            try:
                msg = self._to_gui.get_nowait()
            except queue.Empty:
                break
            mtype = msg.get("type")
            if mtype == "connected":
                self._connected = True
                self._lbl_link.config(text=f"connected ({msg['port']})", fg=CLR_GREEN)
                self._btn_connect.config(text="Disconnect", bg=CLR_RED, fg=CLR_TEXT)
                self._set_buttons_enabled(True)
                self._log_msg(f"[serial] connected to {msg['port']}")
            elif mtype == "disconnected":
                self._connected = False
                self._lbl_link.config(text="disconnected", fg=CLR_RED)
                self._btn_connect.config(text="Connect", bg=CLR_ACCENT, fg="#1e1e2e")
                self._set_buttons_enabled(False)
                self._log_msg("[serial] disconnected")
                self._worker = None
            elif mtype == "state":
                self._recording = bool(msg["recording"])
                self._update_record_ui()
            elif mtype == "pred":
                self._lbl_pred.config(text=msg["label"], fg=CLR_ACCENT)
                self._lbl_conf.config(text=f"{msg['conf']:.1f}%")
            elif mtype == "log":
                self._log_msg(msg["msg"])
            elif mtype == "error":
                self._log_msg(f"[ERR] {msg['msg']}")
        self.after(self.POLL_MS, self._poll)

    def destroy(self) -> None:
        self._disconnect()
        super().destroy()


# ── Entry point ──────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="HAR Nano Serial Desktop Controller")
    ap.add_argument("--port", default=None, help="Serial port (auto-pick if omitted)")
    ap.add_argument("--baud", type=int, default=DEFAULT_BAUD,
                    help=f"Baud rate (default {DEFAULT_BAUD})")
    args = ap.parse_args()

    app = App(port=args.port, baud=args.baud)
    app.mainloop()


if __name__ == "__main__":
    main()
