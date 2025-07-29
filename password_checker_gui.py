import tkinter as tk
from tkinter import messagebox
import re
import math

# Load rockyou.txt
def load_common_passwords(filepath="rockyou.txt"):
    try:
        with open(filepath, 'r', encoding="latin-1") as f:
            return set(line.strip() for line in f if line.strip())
    except:
        return {"123456", "password", "qwerty"}

COMMON_PASSWORDS = load_common_passwords()

def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d", password): charset += 10
    if re.search(r"[!@#$%^&*()_+=\[{\]};:<>|./?,-]", password): charset += 32
    if charset == 0: return 0
    return round(len(password) * math.log2(charset), 2)

def evaluate_password(password):
    score = 0
    issues = []
    suggestions = []

    if password.lower() in COMMON_PASSWORDS:
        issues.append("❌ Too common!")

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        suggestions.append("Use 12+ characters.")
    else:
        issues.append("Too short. Use at least 8 characters.")

    if re.search(r"[a-z]", password): score += 1
    else: suggestions.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password): score += 1
    else: suggestions.append("Add uppercase letters.")

    if re.search(r"\d", password): score += 1
    else: suggestions.append("Include numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
    else: suggestions.append("Add symbols like !@#$%.")

    entropy = calculate_entropy(password)
    if entropy > 60:
        score += 2
    elif entropy > 40:
        score += 1
        suggestions.append("Add more variety for higher entropy.")

    if score >= 8:
        level = ("🟢 Very Strong", "green")
    elif score >= 6:
        level = ("🟡 Strong", "orange")
    elif score >= 4:
        level = ("🟠 Medium", "gold")
    else:
        level = ("🔴 Weak", "red")

    return {
        "score": score,
        "entropy": entropy,
        "strength": level[0],
        "color": level[1],
        "issues": issues,
        "suggestions": suggestions
    }

def toggle_visibility():
    if entry.cget("show") == "":
        entry.config(show="*")
        toggle_btn.config(text="👁 Show")
    else:
        entry.config(show="")
        toggle_btn.config(text="🙈 Hide")

def check_password():
    pwd = entry.get()
    if not pwd:
        messagebox.showerror("Empty", "Please enter a password.")
        return

    result = evaluate_password(pwd)
    result_label.config(text=f"{result['strength']} ({result['score']}/10)", fg=result["color"])
    entropy_label.config(text=f"Entropy: {result['entropy']} bits")

    feedback = ""
    if result["issues"]:
        feedback += "🚫 Issues:\n" + "\n".join(f"• {i}" for i in result["issues"]) + "\n"
    if result["suggestions"]:
        feedback += "\n💡 Suggestions:\n" + "\n".join(f"• {s}" for s in result["suggestions"])
    if not feedback:
        feedback = "✅ Your password is strong and well-formed!"
    feedback_box.config(state="normal")
    feedback_box.delete("1.0", tk.END)
    feedback_box.insert(tk.END, feedback)
    feedback_box.config(state="disabled")

# GUI setup
app = tk.Tk()
app.title("🔐 Advanced Password Strength Checker")
app.geometry("550x500")
app.configure(bg="#f0f4f8")
app.resizable(False, False)

tk.Label(app, text="Enter Password:", font=("Segoe UI", 12), bg="#f0f4f8").pack(pady=(20, 5))

frame = tk.Frame(app, bg="#f0f4f8")
frame.pack()

entry = tk.Entry(frame, show="*", font=("Segoe UI", 12), width=35, bd=2, relief="groove")
entry.pack(side="left", padx=5)

toggle_btn = tk.Button(frame, text="👁 Show", command=toggle_visibility, font=("Segoe UI", 10), width=8)
toggle_btn.pack(side="left")

tk.Button(app, text="Check Strength", command=check_password, bg="#4caf50", fg="white", font=("Segoe UI", 11),
          relief="raised", padx=10, pady=5).pack(pady=15)

result_label = tk.Label(app, text="", font=("Segoe UI", 14, "bold"), bg="#f0f4f8")
result_label.pack()

entropy_label = tk.Label(app, text="", font=("Segoe UI", 10), bg="#f0f4f8")
entropy_label.pack()

tk.Label(app, text="Feedback:", font=("Segoe UI", 12, "underline"), bg="#f0f4f8").pack(pady=10)

feedback_box = tk.Text(app, width=65, height=12, font=("Segoe UI", 10), wrap="word", bg="#ffffff", relief="sunken")
feedback_box.pack()
feedback_box.config(state="disabled")

app.mainloop()
