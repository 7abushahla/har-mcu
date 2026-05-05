#!/usr/bin/env python3
"""
HAR Nano BLE Desktop Controller
================================
Connects to the Arduino Nano 33 BLE running m3_nano_int8_ble_imu.ino and lets
you Start/Stop recording and trigger the long-hold average — all without a
physical shield button.

Requirements:
    pip install bleak

Usage:
    python ble_controller.py
    python ble_controller.py --name HAR-Nano      # connect by device name
    python ble_controller.py --address AA:BB:...  # connect by MAC/UUID directly

BLE protocol (same UUIDs as the .ino):
    cmd  (write)  0x01 = toggle START / STOP
                  0x02 = long-hold average
    status (notify, 2 bytes)
                  byte[0]  0 = idle, 1 = recording
                  byte[1]  last predicted class index (0xFF = none yet)
"""
from __future__ import annotations

import argparse
import asyncio
import queue
import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

from bleak import BleakClient, BleakScanner

# ── BLE UUIDs (must match .ino) ──────────────────────────────────────────────
SERVICE_UUID = "19b10000-e8f2-537e-4f6c-d104768a1214"
CMD_UUID     = "19b10001-e8f2-537e-4f6c-d104768a1214"
STATUS_UUID  = "19b10002-e8f2-537e-4f6c-d104768a1214"

CMD_CLICK    = bytes([0x01])
CMD_LONGHOLD = bytes([0x02])

CLASS_NAMES = ["Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"]

# ── Colour palette ────────────────────────────────────────────────────────────
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


# ── Async BLE worker (runs in its own thread) ─────────────────────────────────
class BleWorker:
    """All bleak calls live here; communicates with the GUI via queues."""

    def __init__(
        self,
        device_name: str | None,
        device_address: str | None,
        to_gui: queue.Queue,
        from_gui: queue.Queue,
    ) -> None:
        self._name = device_name
        self._address = device_address
        self._to_gui = to_gui
        self._from_gui = from_gui
        self._client: BleakClient | None = None
        self._loop: asyncio.AbstractEventLoop | None = None

    # ── public: called from GUI thread ──
    def send_cmd(self, cmd: bytes) -> None:
        if self._loop:
            asyncio.run_coroutine_threadsafe(self._write_cmd(cmd), self._loop)

    def stop(self) -> None:
        if self._loop:
            asyncio.run_coroutine_threadsafe(self._disconnect(), self._loop)

    # ── internal async helpers ──
    def _notify(self, msg: dict) -> None:
        self._to_gui.put_nowait(msg)

    def _status_handler(self, _handle: int, data: bytearray) -> None:
        state = data[0] if len(data) > 0 else 0
        pred  = data[1] if len(data) > 1 else 0xFF
        self._notify({"type": "status", "state": state, "pred": pred})

    async def _write_cmd(self, cmd: bytes) -> None:
        if self._client and self._client.is_connected:
            try:
                await self._client.write_gatt_char(CMD_UUID, cmd, response=False)
            except Exception as exc:
                self._notify({"type": "error", "msg": str(exc)})

    async def _disconnect(self) -> None:
        if self._client and self._client.is_connected:
            await self._client.disconnect()

    async def _run(self) -> None:
        self._notify({"type": "log", "msg": "Scanning for HAR-Nano…"})
        try:
            if self._address:
                device = await BleakScanner.find_device_by_address(
                    self._address, timeout=10.0
                )
            else:
                device = await BleakScanner.find_device_by_name(
                    self._name or "HAR-Nano", timeout=10.0
                )
            if device is None:
                self._notify({"type": "error", "msg": "Device not found. Is the Nano powered and advertising?"})
                return
            self._notify({"type": "log", "msg": f"Found {device.name} ({device.address}) — connecting…"})
            async with BleakClient(device) as client:
                self._client = client
                self._notify({"type": "connected", "address": str(device.address)})
                await client.start_notify(STATUS_UUID, self._status_handler)
                # Drain commands from GUI until disconnect
                while client.is_connected:
                    try:
                        cmd: bytes = self._from_gui.get_nowait()
                        await self._write_cmd(cmd)
                    except queue.Empty:
                        pass
                    await asyncio.sleep(0.02)
        except Exception as exc:
            self._notify({"type": "error", "msg": str(exc)})
        finally:
            self._notify({"type": "disconnected"})

    def run_forever(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self._run())
        self._loop.close()


# ── Tkinter GUI ───────────────────────────────────────────────────────────────
class App(tk.Tk):
    POLL_MS = 50  # how often to drain the BLE→GUI queue

    def __init__(self, device_name: str | None, device_address: str | None) -> None:
        super().__init__()
        self.title("HAR Nano BLE Controller")
        self.configure(bg=CLR_BG)
        self.resizable(False, False)

        self._to_gui:   queue.Queue = queue.Queue()
        self._from_gui: queue.Queue = queue.Queue()
        self._recording = False
        self._connected = False
        self._last_pred: int = 0xFF

        self._worker = BleWorker(device_name, device_address, self._to_gui, self._from_gui)

        self._build_ui()
        self._start_ble_thread()
        self._poll()

    # ── UI construction ──────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        pad = {"padx": 16, "pady": 8}

        # Title
        title_f = tkfont.Font(family="Helvetica", size=16, weight="bold")
        tk.Label(self, text="HAR Nano BLE", font=title_f,
                 bg=CLR_BG, fg=CLR_ACCENT).pack(pady=(18, 2))
        tk.Label(self, text="m3_nano_int8_ble_imu",
                 bg=CLR_BG, fg=CLR_MUTED, font=("Helvetica", 9)).pack()

        # Status bar
        status_frame = tk.Frame(self, bg=CLR_SURFACE, bd=0)
        status_frame.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(status_frame, text="BLE:", bg=CLR_SURFACE,
                 fg=CLR_MUTED, font=("Helvetica", 9)).grid(row=0, column=0, padx=(8, 2), pady=6)
        self._lbl_ble = tk.Label(status_frame, text="disconnected",
                                  bg=CLR_SURFACE, fg=CLR_RED, font=("Helvetica", 9, "bold"))
        self._lbl_ble.grid(row=0, column=1, padx=(0, 16), pady=6, sticky="w")

        tk.Label(status_frame, text="State:", bg=CLR_SURFACE,
                 fg=CLR_MUTED, font=("Helvetica", 9)).grid(row=0, column=2, padx=(8, 2), pady=6)
        self._lbl_state = tk.Label(status_frame, text="idle",
                                    bg=CLR_SURFACE, fg=CLR_MUTED, font=("Helvetica", 9, "bold"))
        self._lbl_state.grid(row=0, column=3, padx=(0, 16), pady=6, sticky="w")

        # Prediction display
        pred_frame = tk.Frame(self, bg=CLR_SURFACE, bd=0)
        pred_frame.pack(fill="x", padx=16, pady=4)
        tk.Label(pred_frame, text="Last prediction",
                 bg=CLR_SURFACE, fg=CLR_MUTED, font=("Helvetica", 9)).pack(pady=(8, 2))
        pred_f = tkfont.Font(family="Helvetica", size=28, weight="bold")
        self._lbl_pred = tk.Label(pred_frame, text="—",
                                   font=pred_f, bg=CLR_SURFACE, fg=CLR_TEXT, width=12)
        self._lbl_pred.pack(pady=(0, 10))

        # Buttons
        btn_frame = tk.Frame(self, bg=CLR_BG)
        btn_frame.pack(padx=16, pady=10)

        btn_style = {"font": ("Helvetica", 13, "bold"), "relief": "flat",
                     "bd": 0, "cursor": "hand2", "width": 10, "pady": 10}

        self._btn_start = tk.Button(
            btn_frame, text="▶  START",
            bg=CLR_START, fg="#1e1e2e",
            command=self._on_click,
            **btn_style,
        )
        self._btn_start.grid(row=0, column=0, padx=6, pady=4)

        self._btn_avg = tk.Button(
            btn_frame, text="⊞  AVERAGE",
            bg=CLR_AVG, fg="#1e1e2e",
            command=self._on_average,
            **btn_style,
        )
        self._btn_avg.grid(row=0, column=1, padx=6, pady=4)

        # Ground truth selector
        gt_frame = tk.Frame(self, bg=CLR_SURFACE, bd=0)
        gt_frame.pack(fill="x", padx=16, pady=(0, 4))
        tk.Label(gt_frame, text="Ground truth (sent via Serial on next START):",
                 bg=CLR_SURFACE, fg=CLR_MUTED, font=("Helvetica", 9)).pack(
                     anchor="w", padx=10, pady=(8, 2))
        self._gt_var = tk.StringVar(value="(none)")
        gt_inner = tk.Frame(gt_frame, bg=CLR_SURFACE)
        gt_inner.pack(padx=6, pady=(0, 8))
        opts = ["(none)"] + CLASS_NAMES
        for i, name in enumerate(opts):
            rb = tk.Radiobutton(
                gt_inner, text=name, variable=self._gt_var, value=name,
                bg=CLR_SURFACE, fg=CLR_TEXT, selectcolor=CLR_BG,
                activebackground=CLR_SURFACE, activeforeground=CLR_ACCENT,
                font=("Helvetica", 10),
            )
            rb.grid(row=i // 4, column=i % 4, sticky="w", padx=6, pady=2)

        # Log box
        log_frame = tk.Frame(self, bg=CLR_BG)
        log_frame.pack(fill="both", padx=16, pady=(4, 16))
        tk.Label(log_frame, text="Log", bg=CLR_BG,
                 fg=CLR_MUTED, font=("Helvetica", 9)).pack(anchor="w")
        self._log = tk.Text(
            log_frame, height=7, bg=CLR_SURFACE, fg=CLR_TEXT,
            font=("Courier", 9), relief="flat", state="disabled",
            wrap="word",
        )
        self._log.pack(fill="both")

        self._set_buttons_enabled(False)

    # ── Button handlers ──────────────────────────────────────────────────────
    def _on_click(self) -> None:
        self._from_gui.put_nowait(CMD_CLICK)
        # optimistic local toggle (BLE status update will confirm)
        self._recording = not self._recording
        self._update_record_ui()

    def _on_average(self) -> None:
        self._from_gui.put_nowait(CMD_LONGHOLD)
        self._log_msg("[GUI] Long-hold average requested")

    # ── BLE state helpers ────────────────────────────────────────────────────
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

    # ── Queue polling (runs on tkinter main loop) ────────────────────────────
    def _poll(self) -> None:
        while True:
            try:
                msg = self._to_gui.get_nowait()
            except queue.Empty:
                break
            mtype = msg.get("type")
            if mtype == "connected":
                self._connected = True
                self._lbl_ble.config(text=f"connected ({msg['address']})", fg=CLR_GREEN)
                self._set_buttons_enabled(True)
                self._log_msg(f"[BLE] connected to {msg['address']}")
            elif mtype == "disconnected":
                self._connected = False
                self._lbl_ble.config(text="disconnected", fg=CLR_RED)
                self._set_buttons_enabled(False)
                self._log_msg("[BLE] disconnected")
            elif mtype == "status":
                state = msg["state"]
                pred  = msg["pred"]
                self._recording = bool(state)
                self._update_record_ui()
                if pred != 0xFF and pred < len(CLASS_NAMES):
                    self._last_pred = pred
                    self._lbl_pred.config(text=CLASS_NAMES[pred], fg=CLR_ACCENT)
                    self._log_msg(f"[pred] {CLASS_NAMES[pred]}")
            elif mtype == "error":
                self._log_msg(f"[ERR] {msg['msg']}")
                messagebox.showerror("BLE Error", msg["msg"])
            elif mtype == "log":
                self._log_msg(msg["msg"])
        self.after(self.POLL_MS, self._poll)

    # ── BLE thread ────────────────────────────────────────────────────────────
    def _start_ble_thread(self) -> None:
        t = threading.Thread(target=self._worker.run_forever, daemon=True)
        t.start()

    def destroy(self) -> None:
        self._worker.stop()
        super().destroy()


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="HAR Nano BLE Desktop Controller")
    ap.add_argument("--name",    default="HAR-Nano", help="BLE device name (default: HAR-Nano)")
    ap.add_argument("--address", default=None,       help="BLE device address (overrides --name)")
    args = ap.parse_args()

    app = App(device_name=args.name, device_address=args.address)
    app.mainloop()


if __name__ == "__main__":
    main()
