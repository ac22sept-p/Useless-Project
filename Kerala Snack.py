"""
╔══════════════════════════════════════════════════════════╗
║   KERALA SNACK AUTHENTICATOR™  (CUSTOMTKINTER EDITION)  ║
║   The World's Most Biased Malayali Food AI              ║
║   TinkerHub Useless Projects Edition — DUAL INPUT V3    ║
╚══════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import random
import threading
import time
import cv2
from PIL import Image, ImageTk

try:
    import winsound
    def beep(f=800, d=100):
        threading.Thread(target=lambda: winsound.Beep(f, d), daemon=True).start()
except:
    def beep(f=800, d=100): pass

# Set modern appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Certified Authentic Kerala Snacks
CERTIFIED_MALLU_SNACKS = [
    "pazham pori", "ethakka appam", "parippuvada", "uzhunnuvada", 
    "sukhiyan", "unniyappam", "neyyappam", "kozhukkatta", 
    "ela ada", "bonda", "cutlet", "mutta puffs", "sulaimani"
]

REJECTION_REASONS = [
    "❌ Thatukada Council ee item eppozhe blacklist cheythu. Evidenu veruneda nee oke?",
    "❌ Oru thulli Velichenna poyitu Nendran Banana skin polum illa... Enthu naattukkaarada ithu !!",
    "❌ Bro, ee sadhanamokke aaranu choodu chaya-yil mukki thinnuka? Parayan polum kollilla!",.",
    "❌ Kerala food aanu polum. Nee pottanano? Vayye mone?.",
    "❌ Ammavans at the junction are deeply disappointed in your lifestyle.",
    "❌ Nee onnum orukaalathum gunam pidikilla mone... Thatukada Union 100% confirm cheythu",
    "❌ Chilara Kazhap onnum allale",
    "❌ ennalum nee, poothu pole valarnittum....ippolum....",
]

SCAN_STEPS = [
    "Detecting pure Velichenna (Coconut Oil) percentage...",
    "Measuring sweetness compatibility with Kadum Chaya...",
    "Checking temperature inside glass display cabinet (Almarah)...",
    "Verifying with All-Kerala Thatukada Union...",
    "Consulting local junction tea-master...",
    "Finalizing culinary citizenship status..."
]


class ModernSnackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kerala Snack Authenticator™ — CustomTkinter")
        self.geometry("640x600") # Made slightly taller to fit input options comfortably
        self.resizable(False, False)

        self.snack_name = ""
        self.use_camera_mode = False  # Track if user prefers typing or camera
        self.show_home()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    # --- Screen 1: Home Input Screen ---
    def show_home(self):
        self.clear()
        beep(600, 80)

        # Main container card
        container = ctk.CTkFrame(self, corner_radius=15, fg_color="#182219")
        container.pack(fill="both", expand=True, padx=25, pady=25)

        # Header
        title = ctk.CTkLabel(
            container, 
            text="🍌 KERALA SNACK AUTHENTICATOR ☕", 
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffb300"
        )
        title.pack(pady=(25, 4))

        subtitle = ctk.CTkLabel(
            container, 
            text="Silicon Valley's 'Not-Hotdog' AI, but for God's Own Country", 
            font=ctk.CTkFont(size=12),
            text_color="#8ea893"
        )
        subtitle.pack(pady=(0, 20))

        # --- DUAL INPUT SELECTOR (RADIO BUTTONS) ---
        method_lbl = ctk.CTkLabel(container, text="Choose Verification Method:", font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffffff")
        method_lbl.pack(pady=(5, 5))

        toggle_frame = ctk.CTkFrame(container, fg_color="transparent")
        toggle_frame.pack(pady=(0, 15))

        self.method_var = ctk.StringVar(value="text")
        
        rb_text = ctk.CTkRadioButton(
            toggle_frame, 
            text="Type Food Name / Presets", 
            variable=self.method_var, 
            value="text",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13),
            fg_color="#ffb300",
            hover_color="#ffa000",
            command=self.toggle_input_fields
        )
        rb_text.pack(side="left", padx=20)

        rb_cam = ctk.CTkRadioButton(
            toggle_frame, 
            text="Scan via Live Camera", 
            variable=self.method_var, 
            value="camera",
            text_color="#ffffff",
            font=ctk.CTkFont(size=13),
            fg_color="#ffb300",
            hover_color="#ffa000",
            command=self.toggle_input_fields
        )
        rb_cam.pack(side="left", padx=20)

        # --- CONTAINER A: TEXT INPUT FIELDS ---
        self.text_container = ctk.CTkFrame(container, fg_color="transparent")
        self.text_container.pack(fill="x", padx=40)

        prompt = ctk.CTkLabel(
            self.text_container, 
            text="Enter the snack you are currently eating or craving:", 
            font=ctk.CTkFont(size=13),
            text_color="#8ea893"
        )
        prompt.pack(pady=(5, 5))

        self.snack_entry = ctk.CTkEntry(
            self.text_container, 
            placeholder_text="e.g. Shawarma, Pazham Pori, Burger...",
            width=320, 
            height=45, 
            font=ctk.CTkFont(size=16),
            corner_radius=10,
            justify="center",
            fg_color="#0f1710",
            border_color="#ffb300"
        )
        self.snack_entry.pack(pady=(0, 10))
        self.snack_entry.insert(0, "Shawarma")
        self.snack_entry.focus()
        self.snack_entry.bind("<Return>", lambda e: self.start_check())

        lbl_presets = ctk.CTkLabel(self.text_container, text="Quick Presets to Test:", font=ctk.CTkFont(size=11), text_color="#8ea893")
        lbl_presets.pack(pady=(5, 4))

        preset_box = ctk.CTkFrame(self.text_container, fg_color="transparent")
        preset_box.pack(pady=(0, 10))

        presets = ["Pazham Pori", "Shawarma", "Parippuvada", "Pizza", "Unniyappam", "Burger"]
        for p in presets:
            btn = ctk.CTkButton(
                preset_box, 
                text=p, 
                width=85, 
                height=30, 
                corner_radius=8,
                fg_color="#0f1710",
                hover_color="#2b3d2c",
                text_color="#ffb300",
                font=ctk.CTkFont(size=11),
                command=lambda item=p: self.quick_select(item)
            )
            btn.pack(side="left", padx=4)

        # --- CONTAINER B: CAMERA MODE MESSAGE ---
        self.cam_container = ctk.CTkFrame(container, fg_color="#0f1710", corner_radius=10, width=340, height=70)
        
        cam_info_lbl = ctk.CTkLabel(
            self.cam_container, 
            text="📷 System webcam will turn on automatically.\nHold your snack up to the lens when the scan begins!", 
            font=ctk.CTkFont(size=12, weight="bold"), 
            text_color="#ffb300",
            justify="center"
        )
        cam_info_lbl.pack(pady=15, padx=20)

        # --- BIG SCAN BUTTON ---
        self.scan_btn = ctk.CTkButton(
            container, 
            text="SCAN TYPED FOOD NAME 🔍", 
            width=280, 
            height=50, 
            corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#ffb300",
            hover_color="#ffa000",
            text_color="#000000",
            command=self.start_check
        )
        self.scan_btn.pack(side="bottom", pady=(10, 20))

        # Initial call to sync visible layouts based on default selection
        self.toggle_input_fields()

    def toggle_input_fields(self):
        """Swaps UI view containers smoothly depending on selected mode."""
        if self.method_var.get() == "text":
            self.cam_container.pack_forget()
            self.text_container.pack(fill="x", padx=40)
            self.scan_btn.configure(text="SCAN TYPED FOOD NAME 🔍")
            self.use_camera_mode = False
        else:
            self.text_container.pack_forget()
            self.cam_container.pack(pady=(10, 20), padx=40)
            self.scan_btn.configure(text="OPEN CAMERA & SCAN SNACK 📸")
            self.use_camera_mode = True

    def quick_select(self, item):
        self.snack_entry.delete(0, "end")
        self.snack_entry.insert(0, item)

    def start_check(self):
        if self.use_camera_mode:
            self.snack_name = "Camera Capture"
        else:
            s = self.snack_entry.get().strip()
            if not s: return
            self.snack_name = s
            
        beep(900, 80)
        self.show_scanner()

    # --- Screen 2: Scanning Progress (With Active Snack Profiling) ---
    def show_scanner(self):
        self.clear()
        self.is_scanning = True
        self.latest_frame = None

        container = ctk.CTkFrame(self, corner_radius=15, fg_color="#182219")
        container.pack(fill="both", expand=True, padx=25, pady=25)

        display_title = "SCANNING LIVE CAMERA STREAM" if self.use_camera_mode else f'INSPECTING "{self.snack_name.upper()}"'
        title = ctk.CTkLabel(
            container, 
            text=f'{display_title}...', 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffb300"
        )
        title.pack(pady=(15, 10))

        # --- CAMERA FEED VIEWPORT ---
        self.cam_label = ctk.CTkLabel(
            container, 
            text="[ Initializing Thatukada Neural Scanner... ]" if not self.use_camera_mode else "[ Booting System Camera... ]", 
            fg_color="#0f1710", 
            width=360, 
            height=200, 
            corner_radius=10
        )
        self.cam_label.pack(pady=(0, 15))

        if self.use_camera_mode:
            self.cap = cv2.VideoCapture(0)
            self.update_camera_feed()

        # Modern CustomTkinter Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            container, 
            width=420, 
            height=16, 
            corner_radius=8,
            progress_color="#ffb300",
            fg_color="#0f1710"
        )
        self.progress_bar.pack(pady=(0, 5))
        self.progress_bar.set(0)

        self.pct_label = ctk.CTkLabel(
            container, 
            text="0%", 
            font=ctk.CTkFont(family="Courier", size=14, weight="bold"),
            text_color="#ffb300"
        )
        self.pct_label.pack(pady=2)

        self.step_label = ctk.CTkLabel(
            container, 
            text="Initializing Thatukada Neural Scanner...", 
            font=ctk.CTkFont(size=13),
            text_color="#8ea893"
        )
        self.step_label.pack(pady=(5, 0))

        self._run_scan(0)

    def update_camera_feed(self):
        """Continuously pulls live frames from the webcam."""
        if self.is_scanning and hasattr(self, 'cap') and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (360, 200))
                self.latest_frame = frame.copy()
                
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.cam_label.imgtk = imgtk
                self.cam_label.configure(image=imgtk, text="")
                
            self.after(20, self.update_camera_feed)

    def _run_scan(self, idx):
        if not self.is_scanning: return
        steps = SCAN_STEPS
        total_steps = len(steps)

        if idx < total_steps:
            if self.use_camera_mode and idx == 3:
                self.step_label.configure(text="⚠️ Scanning item texture... Is that a human face?!")
            else:
                self.step_label.configure(text=f"⟳  {steps[idx]}")
                
            beep(480 + idx * 50, 45)
            target_val = (idx + 1) / total_steps
            current_val = idx / total_steps

            def animate(val):
                if not self.is_scanning: return
                if val <= target_val:
                    self.progress_bar.set(val)
                    self.pct_label.configure(text=f"{int(val * 100)}%")
                    self.after(15, lambda: animate(val + 0.02))
                else:
                    self.after(200, lambda: self._run_scan(idx + 1))

            animate(current_val)
        else:
            self.progress_bar.set(1.0)
            self.pct_label.configure(text="100%")
            
            self.is_scanning = False
            if hasattr(self, 'cap') and self.cap and self.cap.isOpened():
                self.cap.release()
                
            self.after(300, self.show_verdict)


    # --- Screen 3: The Verdict (With Color Validation) ---
    def show_verdict(self):
        self.clear()
        import cv2
        from PIL import Image, ImageTk

        container = ctk.CTkFrame(self, corner_radius=15, fg_color="#182219")
        container.pack(fill="both", expand=True, padx=25, pady=25)

        is_mallu = False
        display_name = ""

        if self.use_camera_mode:
            display_name = "Camera Capture"
            if self.latest_frame is not None:
                try:
                    # --- SAFE COLOR ANALYSIS ROUTINE ---
                    hsv = cv2.cvtColor(self.latest_frame, cv2.COLOR_BGR2HSV)
                    
                    # Broad spectrum representing golden/brown fried snack skin variations
                    lower_gold = (10, 40, 40)
                    upper_gold = (28, 255, 255)
                    
                    mask = cv2.inRange(hsv, lower_gold, upper_gold)
                    gold_pixel_count = cv2.countNonZero(mask)
                    total_pixels = 360 * 200
                    gold_ratio = gold_pixel_count / total_pixels
                    
                    # If enough golden/brown color is seen, consider it a snack!
                    if gold_ratio > 0.08:
                        is_mallu = random.random() < 0.50
                    else:
                        is_mallu = False
                            
                except Exception as e:
                    # Failsafe default so it NEVER goes blank or crashes
                    is_mallu = random.random() < 0.35
            else:
                is_mallu = False
        else:
            n = self.snack_name.lower().strip()
            is_mallu = any(snack in n for snack in CERTIFIED_MALLU_SNACKS)
            display_name = self.snack_name.title()

        # --- SCENARIO EVALUATIONS ---
        if is_mallu:
            beep(800, 100)
            self.after(120, lambda: beep(1200, 150))
            badge_text = "✅ CERTIFIED 100% PURE KERALA SNACK"
            badge_color = "#00e676"
            sub_text = "APPROVED BY KERALA STATE CHAYA SAMITHI ☕"
            sub_color = "#ffb300"
            desc = f"'{display_name}' has passed all strict Nendran Banana and Velichenna texture benchmarks. Consume alongside a boiling hot tea."
            advice = "Recommendation: Dip it into the tea before every single bite."
        else:
            beep(250, 250)
            self.after(280, lambda: beep(200, 300))
            badge_text = "ANARTHAM! Western Imperialist Food Detected!"
            badge_color = "#ff3d00"
            sub_text = random.choice(REJECTION_REASONS)
            sub_color = "#ff5252"
            desc = f"The scanning array determined '{display_name}' is an imposter or non-snack item. No authentic local tea shop will allow this inside their glass showcase cabinet."
            advice = "Recommendation: Throw this away and buy two Parippuvadas immediately."

        # --- CAMERA EVIDENCE SNAPSHOT RENDER ---
        if self.use_camera_mode and self.latest_frame is not None:
            try:
                border_color = (118, 230, 0) if is_mallu else (0, 61, 255)
                snapshot = cv2.copyMakeBorder(self.latest_frame, 6, 6, 6, 6, cv2.BORDER_CONSTANT, value=border_color)
                snapshot = cv2.resize(snapshot, (240, 130))
                
                rgb_snap = cv2.cvtColor(snapshot, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_snap)
                imgtk = ImageTk.PhotoImage(image=img)
                
                lbl_photo = ctk.CTkLabel(container, text="", image=imgtk, corner_radius=8)
                lbl_photo.imgtk = imgtk
                lbl_photo.pack(pady=(15, 0))
            except:
                pass 

        # Output Layout Labels
        header = ctk.CTkLabel(container, text=badge_text, font=ctk.CTkFont(size=16, weight="bold"), text_color=badge_color)
        header.pack(pady=(15, 4))

        sub_lbl = ctk.CTkLabel(container, text=sub_text, font=ctk.CTkFont(size=12, weight="bold"), text_color=sub_color, wraplength=500)
        sub_lbl.pack(pady=(0, 12))

        card = ctk.CTkFrame(container, fg_color="#0f1710", corner_radius=12)
        card.pack(fill="x", padx=40, pady=(0, 15))

        desc_lbl = ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=12), text_color="#ffffff", wraplength=440, justify="center")
        desc_lbl.pack(padx=20, pady=(12, 8))

        adv_lbl = ctk.CTkLabel(card, text=advice, font=ctk.CTkFont(family="Courier", size=11, weight="bold"), text_color="#ffb300" if is_mallu else "#8ea893", wraplength=440)
        adv_lbl.pack(padx=20, pady=(0, 12))

        # Bottom control buttons
        btn_box = ctk.CTkFrame(container, fg_color="transparent")
        btn_box.pack(pady=5)

        retry_btn = ctk.CTkButton(
            btn_box, 
            text="Test Another Snack", 
            width=160, 
            height=38, 
            corner_radius=8,
            fg_color="#2b3d2c",
            hover_color="#3c543e",
            command=self.show_home
        )
        retry_btn.pack(side="left", padx=10)

        exit_btn = ctk.CTkButton(
            btn_box, 
            text="Go to nearest Thatukada (EXIT)", 
            width=140, 
            height=38, 
            corner_radius=8,
            fg_color="#0f1710",
            hover_color="#1e2d20",
            command=self.destroy
        )
        exit_btn.pack(side="left", padx=10)


if __name__ == "__main__":
    app = ModernSnackApp()
    app.mainloop()
