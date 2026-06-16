# ─────────────────────────────────────────────────────────────────
#  My Bank — Tkinter GUI Application
#  Converted from My_Bank_OOP_Corrected.py
#  Features: Login, Dashboard, Check Balance, Withdraw, Deposit,
#            Create Account, Search Accounts, Transaction History
#  Storage : bank_data.json (persistent)
#  Theme   : Dark with accent colours
# ─────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bank_data.json")

# ── Colour palette ───────────────────────────────────────────────
BG_DARK       = "#0f1117"
BG_CARD       = "#1a1d27"
BG_INPUT      = "#252836"
BG_HOVER      = "#2a2d3a"
FG_PRIMARY    = "#e4e6f0"
FG_SECONDARY  = "#8b8fa3"
FG_HEADING    = "#ffffff"
ACCENT_BLUE   = "#4f8cff"
ACCENT_GREEN  = "#34d399"
ACCENT_RED    = "#f87171"
ACCENT_AMBER  = "#fbbf24"
ACCENT_PURPLE = "#a78bfa"
ACCENT_CYAN   = "#22d3ee"
BORDER_COLOR  = "#2e3244"

# ── Fonts ────────────────────────────────────────────────────────
FONT_HEADING  = ("Segoe UI", 22, "bold")
FONT_SUBHEAD  = ("Segoe UI", 14, "bold")
FONT_BODY     = ("Segoe UI", 11)
FONT_BODY_B   = ("Segoe UI", 11, "bold")
FONT_SMALL    = ("Segoe UI", 9)
FONT_BUTTON   = ("Segoe UI", 12, "bold")
FONT_BIG_NUM  = ("Segoe UI", 28, "bold")


# ═══════════════════════════════════════════════════════════════
#  DATA LAYER  – JSON read / write
# ═══════════════════════════════════════════════════════════════
def load_data():
    """Load bank data from JSON file, or return defaults."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "accounts": [
            {"CustomerName": "Nofil",   "AccountNumber": 245645, "AccountType": "Savings Account", "BankBalance": 10000},
            {"CustomerName": "Mujtaba", "AccountNumber": 24555,  "AccountType": "Current Account", "BankBalance": 1000},
        ],
        "transactions": [],
        "next_account_number": 300000,
    }


def save_data(data):
    """Persist bank data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def log_transaction(data, acc_num, txn_type, amount, balance_after):
    """Append a transaction record."""
    data.setdefault("transactions", []).append({
        "AccountNumber": acc_num,
        "Type": txn_type,
        "Amount": amount,
        "BalanceAfter": balance_after,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    save_data(data)


# ═══════════════════════════════════════════════════════════════
#  HELPER WIDGETS
# ═══════════════════════════════════════════════════════════════
class RoundedButton(tk.Canvas):
    """A flat, coloured button with hover animation."""

    def __init__(self, parent, text, command, color=ACCENT_BLUE, width=220, height=48, bg=BG_CARD):
        super().__init__(parent, width=width, height=height,
                         bg=bg, highlightthickness=0, bd=0)
        self._color = color
        self._hover = self._lighten(color, 30)
        self._cmd = command
        self._btn_w = width
        self._btn_h = height
        self._text = text
        self._draw(self._color)
        self.bind("<Enter>", lambda e: self._draw(self._hover))
        self.bind("<Leave>", lambda e: self._draw(self._color))
        self.bind("<Button-1>", lambda e: self._cmd())

    def _draw(self, fill):
        self.delete("all")
        r = 12
        w, h = self._btn_w, self._btn_h
        # Rounded rectangle
        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=fill, outline="")
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=fill, outline="")
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=fill, outline="")
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=fill, outline="")
        self.create_rectangle(r, 0, w-r, h, fill=fill, outline="")
        self.create_rectangle(0, r, w, h-r, fill=fill, outline="")
        self.create_text(w//2, h//2, text=self._text, fill="#ffffff", font=FONT_BUTTON)

    @staticmethod
    def _lighten(hex_col, amount):
        r, g, b = int(hex_col[1:3], 16), int(hex_col[3:5], 16), int(hex_col[5:7], 16)
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
        return f"#{r:02x}{g:02x}{b:02x}"


def styled_entry(parent, placeholder="", show="", width=30):
    """Create a dark‑themed entry with a placeholder."""
    var = tk.StringVar()
    entry = tk.Entry(
        parent, textvariable=var, font=FONT_BODY,
        bg=BG_INPUT, fg=FG_PRIMARY, insertbackground=FG_PRIMARY,
        relief="flat", bd=0, highlightthickness=2,
        highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_BLUE,
        width=width,
    )
    if show:
        entry.config(show=show)

    # Placeholder behaviour
    if placeholder:
        def _on_focus_in(e):
            if var.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=FG_PRIMARY)
                if show:
                    entry.config(show=show)

        def _on_focus_out(e):
            if not var.get():
                entry.insert(0, placeholder)
                entry.config(fg=FG_SECONDARY, show="")

        entry.insert(0, placeholder)
        entry.config(fg=FG_SECONDARY, show="")
        entry.bind("<FocusIn>", _on_focus_in)
        entry.bind("<FocusOut>", _on_focus_out)

    return entry, var


def make_label(parent, text, font=FONT_BODY, fg=FG_PRIMARY, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=BG_CARD, **kw)


def center_window(win, w, h):
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


# ═══════════════════════════════════════════════════════════════
#  LOGIN WINDOW
# ═══════════════════════════════════════════════════════════════
class LoginWindow:
    ADMIN_USER = "admin"
    ADMIN_PASS = "1234"

    def __init__(self, root):
        self.root = root
        self.root.title("My Bank — Login")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        center_window(self.root, 440, 520)

        # ── Card frame ──
        card = tk.Frame(self.root, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=440)

        # Icon / emoji
        tk.Label(card, text="🏦", font=("Segoe UI Emoji", 40), bg=BG_CARD).pack(pady=(30, 5))

        # Title
        tk.Label(card, text="My Bank", font=FONT_HEADING, fg=ACCENT_BLUE, bg=BG_CARD).pack()
        tk.Label(card, text="Sign in to continue", font=FONT_SMALL, fg=FG_SECONDARY, bg=BG_CARD).pack(pady=(0, 25))

        # Username
        make_label(card, "Username", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=40)
        self.user_entry, self.user_var = styled_entry(card, placeholder="admin", width=28)
        self.user_entry.pack(padx=40, pady=(2, 15), ipady=6)

        # Password
        make_label(card, "Password", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=40)
        self.pass_entry, self.pass_var = styled_entry(card, placeholder="••••", show="•", width=28)
        self.pass_entry.pack(padx=40, pady=(2, 25), ipady=6)

        # Login button
        btn = RoundedButton(card, "Sign In", self._login, ACCENT_BLUE, width=300, height=46)
        btn.pack()

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self._login())

    # ──────────────────────────
    def _get_field(self, var, placeholder):
        val = var.get().strip()
        return "" if val == placeholder else val

    def _login(self):
        user = self._get_field(self.user_var, "admin")
        pwd  = self._get_field(self.pass_var, "••••")

        # If fields still show placeholder text and haven't been focused, treat as empty
        if not user:
            user = self.user_var.get().strip()
            if user == "admin":
                # Could be the placeholder OR the actual typed value
                # Check foreground colour to distinguish
                if self.user_entry.cget("fg") == FG_SECONDARY:
                    user = ""
        if not pwd:
            pwd = self.pass_var.get().strip()
            if pwd == "••••" and self.pass_entry.cget("fg") == FG_SECONDARY:
                pwd = ""

        if user == self.ADMIN_USER and pwd == self.ADMIN_PASS:
            self.root.destroy()
            launch_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.\n\nHint: admin / 1234")


# ═══════════════════════════════════════════════════════════════
#  DASHBOARD
# ═══════════════════════════════════════════════════════════════
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("My Bank — Dashboard")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)
        center_window(self.root, 700, 660)

        self.data = load_data()

        # ── Scrollable container ──
        container = tk.Frame(self.root, bg=BG_DARK)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview,
                                 bg=BG_DARK, troughcolor=BG_DARK, activebackground=ACCENT_BLUE)
        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Unbind mousewheel when dashboard is destroyed
        self.root.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"), add="+")

        # ── Header ──
        header = tk.Frame(scroll_frame, bg=BG_DARK)
        header.pack(fill="x", padx=30, pady=(25, 5))
        tk.Label(header, text="🏦", font=("Segoe UI Emoji", 26), bg=BG_DARK).pack(side="left")
        tk.Label(header, text="  My Bank Dashboard", font=FONT_HEADING, fg=FG_HEADING, bg=BG_DARK).pack(side="left")

        tk.Label(scroll_frame, text="Select an operation to get started",
                 font=FONT_BODY, fg=FG_SECONDARY, bg=BG_DARK).pack(anchor="w", padx=36, pady=(0, 20))

        # ── Buttons grid ──
        grid = tk.Frame(scroll_frame, bg=BG_DARK)
        grid.pack(padx=30)

        buttons_info = [
            ("💰  Check Balance",    ACCENT_BLUE,   self._check_balance),
            ("📤  Withdraw",         ACCENT_RED,    self._withdraw),
            ("📥  Deposit",          ACCENT_GREEN,  self._deposit),
            ("➕  Create Account",   ACCENT_PURPLE, self._create_account),
            ("🔎  All Accounts",     ACCENT_CYAN,   self._search_accounts),
            ("📋  Transaction Log",  ACCENT_AMBER,  self._transaction_history),
            ("🗑️  Delete Account",   ACCENT_RED,    self._delete_account),
        ]

        for idx, (text, color, cmd) in enumerate(buttons_info):
            row, col = divmod(idx, 2)
            card = tk.Frame(grid, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            inner = tk.Frame(card, bg=BG_CARD)
            inner.pack(padx=15, pady=18)

            tk.Label(inner, text=text.split("  ")[0], font=("Segoe UI Emoji", 28), bg=BG_CARD).pack()
            btn = RoundedButton(inner, text.split("  ")[1], cmd, color, width=260, height=44)
            btn.pack(pady=(8, 0))

        # ── Footer ──
        tk.Label(scroll_frame, text="Data is auto‑saved to bank_data.json",
                 font=FONT_SMALL, fg=FG_SECONDARY, bg=BG_DARK).pack(pady=12)

    # ── Helpers ──────────────────────────────────────────────
    def _find_account(self, acc_num):
        for acc in self.data["accounts"]:
            if acc["AccountNumber"] == acc_num:
                return acc
        return None

    def _popup(self, title, width=420, height=340):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=BG_CARD)
        win.resizable(True, True)
        center_window(win, width, height)
        win.grab_set()
        return win

    # ── 1. Check Balance ────────────────────────────────────
    def _check_balance(self):
        win = self._popup("Check Balance", 440, 320)

        tk.Label(win, text="💰 Check Balance", font=FONT_SUBHEAD, fg=ACCENT_BLUE, bg=BG_CARD).pack(pady=(25, 15))
        make_label(win, "Account Number", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        entry, var = styled_entry(win, width=26)
        entry.pack(padx=50, pady=(2, 20), ipady=6)

        result_lbl = tk.Label(win, text="", font=FONT_BIG_NUM, fg=ACCENT_GREEN, bg=BG_CARD)
        result_lbl.pack(pady=(0, 5))
        sub_lbl = tk.Label(win, text="", font=FONT_SMALL, fg=FG_SECONDARY, bg=BG_CARD)
        sub_lbl.pack()

        def check():
            try:
                acc_num = int(var.get())
            except ValueError:
                messagebox.showwarning("Invalid Input", "Please enter a valid account number.", parent=win)
                return
            acc = self._find_account(acc_num)
            if acc:
                result_lbl.config(text=f"Rs {acc['BankBalance']:,}")
                sub_lbl.config(text=f"{acc['CustomerName']}  •  {acc['AccountType']}")
            else:
                messagebox.showerror("Not Found", "Account not found.", parent=win)

        btn = RoundedButton(win, "Check", check, ACCENT_BLUE, width=300, height=42)
        btn.pack()

    # ── 2. Withdraw ─────────────────────────────────────────
    def _withdraw(self):
        win = self._popup("Withdraw", 440, 360)

        tk.Label(win, text="📤 Withdraw", font=FONT_SUBHEAD, fg=ACCENT_RED, bg=BG_CARD).pack(pady=(25, 15))

        make_label(win, "Account Number", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        acc_entry, acc_var = styled_entry(win, width=26)
        acc_entry.pack(padx=50, pady=(2, 12), ipady=6)

        make_label(win, "Withdraw Amount", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        amt_entry, amt_var = styled_entry(win, width=26)
        amt_entry.pack(padx=50, pady=(2, 20), ipady=6)

        def withdraw():
            try:
                acc_num = int(acc_var.get())
                amount = int(amt_var.get())
            except ValueError:
                messagebox.showwarning("Invalid Input", "Enter valid numbers.", parent=win)
                return
            if amount <= 0:
                messagebox.showwarning("Invalid Amount", "Amount must be positive.", parent=win)
                return
            acc = self._find_account(acc_num)
            if not acc:
                messagebox.showerror("Not Found", "Account not found.", parent=win)
                return
            if acc["BankBalance"] < amount:
                messagebox.showerror("Insufficient Funds",
                    f"Balance is Rs {acc['BankBalance']:,}.\nCannot withdraw Rs {amount:,}.", parent=win)
                return
            acc["BankBalance"] -= amount
            log_transaction(self.data, acc_num, "Withdrawal", amount, acc["BankBalance"])
            messagebox.showinfo("Success",
                f"Withdrawn Rs {amount:,}\nNew balance: Rs {acc['BankBalance']:,}", parent=win)
            win.destroy()

        btn = RoundedButton(win, "Withdraw", withdraw, ACCENT_RED, width=300, height=42)
        btn.pack()

    # ── 3. Deposit ──────────────────────────────────────────
    def _deposit(self):
        win = self._popup("Deposit", 440, 360)

        tk.Label(win, text="📥 Deposit", font=FONT_SUBHEAD, fg=ACCENT_GREEN, bg=BG_CARD).pack(pady=(25, 15))

        make_label(win, "Account Number", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        acc_entry, acc_var = styled_entry(win, width=26)
        acc_entry.pack(padx=50, pady=(2, 12), ipady=6)

        make_label(win, "Deposit Amount", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        amt_entry, amt_var = styled_entry(win, width=26)
        amt_entry.pack(padx=50, pady=(2, 20), ipady=6)

        def deposit():
            try:
                acc_num = int(acc_var.get())
                amount = int(amt_var.get())
            except ValueError:
                messagebox.showwarning("Invalid Input", "Enter valid numbers.", parent=win)
                return
            if amount <= 0:
                messagebox.showwarning("Invalid Amount", "Amount must be positive.", parent=win)
                return
            acc = self._find_account(acc_num)
            if not acc:
                messagebox.showerror("Not Found", "Account not found.", parent=win)
                return
            acc["BankBalance"] += amount
            log_transaction(self.data, acc_num, "Deposit", amount, acc["BankBalance"])
            messagebox.showinfo("Success",
                f"Deposited Rs {amount:,}\nNew balance: Rs {acc['BankBalance']:,}", parent=win)
            win.destroy()

        btn = RoundedButton(win, "Deposit", deposit, ACCENT_GREEN, width=300, height=42)
        btn.pack()

    # ── 4. Create Account ───────────────────────────────────
    def _create_account(self):
        win = self._popup("Create Account", 440, 420)

        tk.Label(win, text="➕ Create Account", font=FONT_SUBHEAD, fg=ACCENT_PURPLE, bg=BG_CARD).pack(pady=(20, 12))

        make_label(win, "Customer Name", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        name_entry, name_var = styled_entry(win, width=26)
        name_entry.pack(padx=50, pady=(2, 10), ipady=6)

        make_label(win, "Account Type", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        type_var = tk.StringVar(value="Savings Account")
        type_frame = tk.Frame(win, bg=BG_CARD)
        type_frame.pack(padx=50, anchor="w", pady=(2, 10))
        for val in ("Savings Account", "Current Account"):
            tk.Radiobutton(type_frame, text=val, variable=type_var, value=val,
                           bg=BG_CARD, fg=FG_PRIMARY, selectcolor=BG_INPUT,
                           activebackground=BG_CARD, activeforeground=FG_PRIMARY,
                           font=FONT_BODY).pack(side="left", padx=(0, 15))

        make_label(win, "Initial Deposit", font=FONT_BODY_B, fg=FG_SECONDARY).pack(anchor="w", padx=50)
        dep_entry, dep_var = styled_entry(win, width=26)
        dep_entry.pack(padx=50, pady=(2, 20), ipady=6)

        def create():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Missing Name", "Enter customer name.", parent=win)
                return
            try:
                deposit = int(dep_var.get())
            except ValueError:
                messagebox.showwarning("Invalid Input", "Enter a valid deposit amount.", parent=win)
                return
            if deposit < 0:
                messagebox.showwarning("Invalid Amount", "Deposit cannot be negative.", parent=win)
                return

            acc_num = self.data.get("next_account_number", 300000)
            new_acc = {
                "CustomerName": name,
                "AccountNumber": acc_num,
                "AccountType": type_var.get(),
                "BankBalance": deposit,
            }
            self.data["accounts"].append(new_acc)
            self.data["next_account_number"] = acc_num + 1
            log_transaction(self.data, acc_num, "Account Created", deposit, deposit)
            messagebox.showinfo("Account Created",
                f"Account created successfully!\n\n"
                f"Name: {name}\n"
                f"Account #: {acc_num}\n"
                f"Type: {type_var.get()}\n"
                f"Balance: Rs {deposit:,}", parent=win)
            win.destroy()

        btn = RoundedButton(win, "Create Account", create, ACCENT_PURPLE, width=300, height=42)
        btn.pack()

    # ── 5. Search All Accounts ──────────────────────────────
    def _search_accounts(self):
        win = self._popup("All Accounts", 640, 440)

        tk.Label(win, text="🔎 All Accounts", font=FONT_SUBHEAD, fg=ACCENT_CYAN, bg=BG_CARD).pack(pady=(15, 10))

        # ── Treeview with dark theme ──
        style = ttk.Style(win)
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                         background=BG_INPUT, foreground=FG_PRIMARY, fieldbackground=BG_INPUT,
                         borderwidth=0, font=FONT_BODY, rowheight=32)
        style.configure("Dark.Treeview.Heading",
                         background=BG_DARK, foreground=ACCENT_CYAN, font=FONT_BODY_B,
                         borderwidth=0)
        style.map("Dark.Treeview", background=[("selected", ACCENT_BLUE)])

        cols = ("Name", "Account #", "Type", "Balance")
        tree = ttk.Treeview(win, columns=cols, show="headings", style="Dark.Treeview", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=140)

        for acc in self.data["accounts"]:
            tree.insert("", "end", values=(
                acc["CustomerName"], acc["AccountNumber"],
                acc["AccountType"], f"Rs {acc['BankBalance']:,}"))

        tree.pack(padx=15, pady=(0, 10), fill="both", expand=True)

        # Scrollbar
        sb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)

        count_text = f"Total accounts: {len(self.data['accounts'])}"
        tk.Label(win, text=count_text, font=FONT_SMALL, fg=FG_SECONDARY, bg=BG_CARD).pack(pady=(0, 10))

    # ── 6. Transaction History ──────────────────────────────
    def _transaction_history(self):
        win = self._popup("Transaction History", 680, 460)

        tk.Label(win, text="📋 Transaction History", font=FONT_SUBHEAD, fg=ACCENT_AMBER, bg=BG_CARD).pack(pady=(15, 10))

        style = ttk.Style(win)
        style.theme_use("clam")
        style.configure("Txn.Treeview",
                         background=BG_INPUT, foreground=FG_PRIMARY, fieldbackground=BG_INPUT,
                         borderwidth=0, font=FONT_BODY, rowheight=30)
        style.configure("Txn.Treeview.Heading",
                         background=BG_DARK, foreground=ACCENT_AMBER, font=FONT_BODY_B,
                         borderwidth=0)
        style.map("Txn.Treeview", background=[("selected", ACCENT_BLUE)])

        cols = ("Timestamp", "Account #", "Type", "Amount", "Balance After")
        tree = ttk.Treeview(win, columns=cols, show="headings", style="Txn.Treeview", height=12)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=125)

        transactions = self.data.get("transactions", [])
        for txn in reversed(transactions):  # newest first
            tree.insert("", "end", values=(
                txn["Timestamp"], txn["AccountNumber"],
                txn["Type"], f"Rs {txn['Amount']:,}",
                f"Rs {txn['BalanceAfter']:,}"))

        tree.pack(padx=15, pady=(0, 10), fill="both", expand=True)

        if not transactions:
            tk.Label(win, text="No transactions yet.", font=FONT_BODY, fg=FG_SECONDARY, bg=BG_CARD).pack()

        count_text = f"Total transactions: {len(transactions)}"
        tk.Label(win, text=count_text, font=FONT_SMALL, fg=FG_SECONDARY, bg=BG_CARD).pack(pady=(0, 10))

    # ── 7. Delete Account ───────────────────────────────────
    def _delete_account(self):
        win = self._popup("Delete Account", 640, 480)

        tk.Label(win, text="🗑️ Delete Account", font=FONT_SUBHEAD, fg=ACCENT_RED, bg=BG_CARD).pack(pady=(15, 5))
        tk.Label(win, text="Select an account from the table, then click Delete",
                 font=FONT_SMALL, fg=FG_SECONDARY, bg=BG_CARD).pack(pady=(0, 10))

        # ── Treeview with dark theme ──
        style = ttk.Style(win)
        style.theme_use("clam")
        style.configure("Del.Treeview",
                         background=BG_INPUT, foreground=FG_PRIMARY, fieldbackground=BG_INPUT,
                         borderwidth=0, font=FONT_BODY, rowheight=32)
        style.configure("Del.Treeview.Heading",
                         background=BG_DARK, foreground=ACCENT_RED, font=FONT_BODY_B,
                         borderwidth=0)
        style.map("Del.Treeview", background=[("selected", ACCENT_RED)])

        cols = ("Name", "Account #", "Type", "Balance")
        tree = ttk.Treeview(win, columns=cols, show="headings", style="Del.Treeview", height=10)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=140)

        for acc in self.data["accounts"]:
            tree.insert("", "end", values=(
                acc["CustomerName"], acc["AccountNumber"],
                acc["AccountType"], f"Rs {acc['BankBalance']:,}"))

        tree.pack(padx=15, pady=(0, 10), fill="both", expand=True)

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("No Selection", "Please select an account to delete.", parent=win)
                return

            item = tree.item(selected[0])
            values = item["values"]
            name = values[0]
            acc_num = int(values[1])

            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete this account?\n\n"
                f"Name: {name}\n"
                f"Account #: {acc_num}\n\n"
                f"This action cannot be undone.\n"
                f"Transaction history will be preserved.",
                parent=win
            )
            if not confirm:
                return

            # Remove the account from data
            self.data["accounts"] = [
                acc for acc in self.data["accounts"]
                if acc["AccountNumber"] != acc_num
            ]
            log_transaction(self.data, acc_num, "Account Deleted", 0, 0)
            messagebox.showinfo("Deleted",
                f"Account #{acc_num} ({name}) has been deleted.", parent=win)
            win.destroy()

        btn = RoundedButton(win, "Delete Selected", delete_selected, ACCENT_RED, width=300, height=42)
        btn.pack(pady=(0, 15))


# ═══════════════════════════════════════════════════════════════
#  LAUNCH HELPERS
# ═══════════════════════════════════════════════════════════════
def launch_dashboard():
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()


def main():
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
