import tkinter as tk
from tkinter import messagebox
import re

def text_to_binary(text):
    return ' '.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    binary = binary.strip()
    binary_values = re.split(r'[\s,]+', binary)
    binary_values = [b for b in binary_values if b]
    
    if not all(re.fullmatch(r'[01]{8}', b) for b in binary_values):
        raise ValueError("Invalid binary input. Each byte must be exactly 8 bits (0s and 1s), separated by spaces.")
    
    return ''.join(chr(int(b, 2)) for b in binary_values)

def convert():
    input_data = input_text.get("1.0", tk.END).strip()
    
    if not input_data:
        messagebox.showwarning("Empty Input", "Please enter some data to convert.")
        return
    
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    
    try:
        if mode_var.get() == "text_to_binary":
            result = text_to_binary(input_data)
        else:
            result = binary_to_text(input_data)
        
        output_text.insert("1.0", result)
        animate_output()
    except ValueError as e:
        messagebox.showerror("Conversion Error", str(e))
    finally:
        output_text.config(state=tk.DISABLED)

def clear_all():
    input_text.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    send_btn.config(state=tk.DISABLED, bg=BTN_BG, fg=FG_GREY)

def animate_output():
    output_frame.config(highlightbackground="#aaaaaa")
    root.after(300, lambda: output_frame.config(highlightbackground="#444444"))
    # Enable send button after successful conversion
    send_btn.config(state=tk.NORMAL, bg=ACCENT, fg="#1a1a1a")

def copy_output():
    content = output_text.get("1.0", tk.END).strip()
    if content:
        root.clipboard_clear()
        root.update()
        root.clipboard_append(content)
        copy_btn.config(text="✓ Copied!")
        root.after(1500, lambda: copy_btn.config(text="⧉ Copy"))

def send_to_input():
    """Send output directly to input and switch mode automatically."""
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Nothing to Send", "There is no output data to send.")
        return

    current_mode = mode_var.get()

    # Switch mode
    if current_mode == "text_to_binary":
        mode_var.set("binary_to_text")
    else:
        mode_var.set("text_to_binary")

    # Update labels for new mode
    on_mode_change()

    # Clear input and paste output content into it
    input_text.delete("1.0", tk.END)
    input_text.insert("1.0", content)

    # Clear output
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

    # Disable send button until next conversion
    send_btn.config(state=tk.DISABLED, bg=BTN_BG, fg=FG_GREY)

    # Flash input to signal transfer
    input_frame.config(highlightbackground="#aaaaaa")
    root.after(300, lambda: input_frame.config(highlightbackground="#444444"))

def on_mode_change():
    selected = mode_var.get()
    if selected == "text_to_binary":
        input_label.config(text="▸ TEXT INPUT")
        output_label.config(text="▸ BINARY OUTPUT")
        input_hint.config(text="Enter plain text here...")
    else:
        input_label.config(text="▸ BINARY INPUT")
        output_label.config(text="▸ TEXT OUTPUT")
        input_hint.config(text="Enter binary (8-bit groups separated by spaces)...")

# ─── Root Window ───────────────────────────────────────────────
root = tk.Tk()
root.title("Binary ↔ Text Converter")
root.geometry("700x760")
root.resizable(False, False)
root.configure(bg="#1a1a1a")

# ─── Fonts ─────────────────────────────────────────────────────
FONT_TITLE    = ("Courier New", 15, "bold")
FONT_LABEL    = ("Courier New", 9, "bold")
FONT_MONO     = ("Courier New", 11)
FONT_HINT     = ("Courier New", 9)
FONT_BTN      = ("Courier New", 10, "bold")
FONT_RADIO    = ("Courier New", 10, "bold")

# ─── Colors ────────────────────────────────────────────────────
BG_DARK       = "#1a1a1a"
BG_PANEL      = "#232323"
BG_FIELD      = "#2e2e2e"
FG_WHITE      = "#f0f0f0"
FG_GREY       = "#888888"
FG_LIGHT      = "#cccccc"
ACCENT        = "#c0c0c0"
BORDER        = "#444444"
BTN_BG        = "#333333"
BTN_ACTIVE    = "#505050"
SEL_BG        = "#505050"

# ─── Title Bar ─────────────────────────────────────────────────
title_frame = tk.Frame(root, bg=BG_DARK, pady=18)
title_frame.pack(fill=tk.X)

tk.Label(
    title_frame,
    text="⬡  BINARY · TEXT  ⬡",
    font=FONT_TITLE,
    bg=BG_DARK,
    fg=ACCENT,
).pack()

tk.Label(
    title_frame,
    text="CONVERSION UTILITY",
    font=("Courier New", 8),
    bg=BG_DARK,
    fg=FG_GREY
).pack()

tk.Frame(root, bg=BORDER, height=1).pack(fill=tk.X, padx=20)

# ─── Input Section ─────────────────────────────────────────────
input_label = tk.Label(root, text="▸ TEXT INPUT", font=FONT_LABEL,
                       bg=BG_DARK, fg=FG_GREY, anchor="w")
input_label.pack(fill=tk.X, padx=28, pady=(18, 4))

input_frame = tk.Frame(root, bg=BORDER, bd=0,
                       highlightthickness=1, highlightbackground=BORDER)
input_frame.pack(fill=tk.X, padx=24)

input_text = tk.Text(
    input_frame, height=6, font=FONT_MONO,
    bg=BG_FIELD, fg=FG_WHITE, insertbackground=ACCENT,
    relief=tk.FLAT, bd=0, padx=10, pady=10,
    selectbackground=SEL_BG, selectforeground=FG_WHITE,
    wrap=tk.WORD
)
input_text.pack(fill=tk.X)

input_hint = tk.Label(root, text="Enter plain text here...",
                      font=FONT_HINT, bg=BG_DARK, fg=FG_GREY, anchor="w")
input_hint.pack(fill=tk.X, padx=30, pady=(4, 0))

# ─── Mode Selector ─────────────────────────────────────────────
mode_frame = tk.Frame(root, bg=BG_DARK, pady=18)
mode_frame.pack()

mode_var = tk.StringVar(value="text_to_binary")

style_opts = dict(
    bg=BG_DARK, fg=FG_LIGHT,
    activebackground=BG_DARK, activeforeground=ACCENT,
    selectcolor=BG_PANEL,
    font=FONT_RADIO, bd=0, highlightthickness=0,
    cursor="hand2"
)

rb1 = tk.Radiobutton(
    mode_frame, text="TEXT → BINARY",
    variable=mode_var, value="text_to_binary",
    command=on_mode_change, **style_opts
)
rb1.grid(row=0, column=0, padx=20)

tk.Label(mode_frame, text="│", font=("Courier New", 14),
         bg=BG_DARK, fg=BORDER).grid(row=0, column=1)

rb2 = tk.Radiobutton(
    mode_frame, text="BINARY → TEXT",
    variable=mode_var, value="binary_to_text",
    command=on_mode_change, **style_opts
)
rb2.grid(row=0, column=2, padx=20)

# ─── Action Buttons ────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG_DARK)
btn_frame.pack(pady=(0, 16))

btn_style = dict(
    font=FONT_BTN, relief=tk.FLAT, bd=0,
    cursor="hand2", padx=18, pady=8
)

convert_btn = tk.Button(
    btn_frame, text="⟳  CONVERT",
    bg=ACCENT, fg="#1a1a1a",
    activebackground=FG_WHITE, activeforeground="#1a1a1a",
    command=convert, **btn_style
)
convert_btn.grid(row=0, column=0, padx=8)

clear_btn = tk.Button(
    btn_frame, text="✕  CLEAR",
    bg=BTN_BG, fg=FG_LIGHT,
    activebackground=BTN_ACTIVE, activeforeground=FG_WHITE,
    command=clear_all, **btn_style
)
clear_btn.grid(row=0, column=1, padx=8)

tk.Frame(root, bg=BORDER, height=1).pack(fill=tk.X, padx=20, pady=(0, 8))

# ─── Output Section ────────────────────────────────────────────
output_label = tk.Label(root, text="▸ BINARY OUTPUT", font=FONT_LABEL,
                        bg=BG_DARK, fg=FG_GREY, anchor="w")
output_label.pack(fill=tk.X, padx=28, pady=(10, 4))

output_frame = tk.Frame(root, bg=BORDER, bd=0,
                        highlightthickness=1, highlightbackground=BORDER)
output_frame.pack(fill=tk.X, padx=24)

output_text = tk.Text(
    output_frame, height=7, font=FONT_MONO,
    bg="#202020", fg="#d4d4d4", insertbackground=ACCENT,
    relief=tk.FLAT, bd=0, padx=10, pady=10,
    selectbackground=SEL_BG, selectforeground=FG_WHITE,
    state=tk.DISABLED, wrap=tk.WORD
)
output_text.pack(fill=tk.X)

# ─── Output Action Row ─────────────────────────────────────────
out_action_frame = tk.Frame(root, bg=BG_DARK)
out_action_frame.pack(fill=tk.X, padx=24, pady=(8, 0))

copy_btn = tk.Button(
    out_action_frame, text="⧉ Copy",
    font=FONT_HINT, bg=BG_DARK, fg=FG_GREY,
    activebackground=BG_DARK, activeforeground=ACCENT,
    relief=tk.FLAT, bd=0, cursor="hand2",
    command=copy_output
)
copy_btn.pack(side=tk.RIGHT, padx=(8, 6))

# ─── Send to Input Button ──────────────────────────────────────
send_btn = tk.Button(
    out_action_frame,
    text="⟵  SEND TO INPUT  &  SWITCH MODE",
    font=FONT_HINT, relief=tk.FLAT, bd=0,
    cursor="hand2", padx=12, pady=5,
    bg=BTN_BG, fg=FG_GREY,
    activebackground=BTN_ACTIVE, activeforeground=FG_WHITE,
    state=tk.DISABLED,
    command=send_to_input
)
send_btn.pack(side=tk.LEFT)

# ─── Info Label ────────────────────────────────────────────────
tk.Label(
    root,
    text="⬡  Convert output → auto-switch mode → paste into input",
    font=("Courier New", 8),
    bg=BG_DARK, fg="#3a3a3a"
).pack(pady=(6, 0))

# ─── Footer ────────────────────────────────────────────────────
tk.Label(
    root,
    text="——— Binary ↔ Text  •  Python Utility ———",
    font=("Courier New", 8),
    bg=BG_DARK, fg="#3a3a3a"
).pack(side=tk.BOTTOM, pady=10)

# ─── Keyboard Shortcuts ────────────────────────────────────────
root.bind("<Return>", lambda e: convert())
root.bind("<Control-l>", lambda e: clear_all())
root.bind("<Control-s>", lambda e: send_to_input())

root.mainloop()