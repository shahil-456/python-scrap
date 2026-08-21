import json
import tkinter as tk

FILE = "bundle.js"

with open(FILE, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("window.__OFFLINE_BUNDLE__ =", "", 1).strip()
data = json.loads(text.rstrip(";"))

questions = data["content"]["questions"]
options = data["content"]["options"]

current = 0


def get_option(option_id):
    return next(x for x in options if x["id"] == option_id)


def show_question():
    q = questions[current]

    counter.config(text=f"{current + 1} / {len(questions)}")
    question.config(text=q["body"])

    for widget in options_frame.winfo_children():
        widget.destroy()

    for i, option_id in enumerate(q["optionIds"]):
        option = get_option(option_id)

        button = tk.Button(
            options_frame,
            text=f"{chr(65 + i)}   {option['body']}",
            anchor="w",
            justify="left",
            wraplength=700,
            font=("Arial", 12),
            padx=15,
            pady=12,
            bg="#14532d" if option.get("isCorrect") else "#1f2937",
            fg="#86efac" if option.get("isCorrect") else "white",
            activebackground="#374151",
            activeforeground="white",
            relief="flat",
            command=lambda oid=option_id: set_answer(oid)
        )

        button.pack(fill="x", pady=5)


def set_answer(selected_id):
    q = questions[current]

    for option_id in q["optionIds"]:
        option = get_option(option_id)
        option["isCorrect"] = option_id == selected_id

    show_question()


def next_question():
    global current

    if current < len(questions) - 1:
        current += 1
        show_question()


def previous_question():
    global current

    if current > 0:
        current -= 1
        show_question()


def save_json():
    with open(FILE, "w", encoding="utf-8") as f:
        f.write("window.__OFFLINE_BUNDLE__ = ")
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write(";")

    status.config(text="Saved!")


root = tk.Tk()
root.title("Set Answers")
root.geometry("850x650")
root.configure(bg="#030712")

counter = tk.Label(
    root,
    text="",
    bg="#030712",
    fg="#9ca3af",
    font=("Arial", 11)
)
counter.pack(pady=(20, 5))

question = tk.Label(
    root,
    text="",
    bg="#111827",
    fg="white",
    font=("Arial", 14, "bold"),
    anchor="w",
    justify="left",
    wraplength=760,
    padx=20,
    pady=20
)
question.pack(fill="x", padx=30, pady=10)

options_frame = tk.Frame(root, bg="#030712")
options_frame.pack(fill="both", expand=True, padx=30)

navigation = tk.Frame(root, bg="#030712")
navigation.pack(fill="x", padx=30, pady=10)

tk.Button(
    navigation,
    text="← Previous",
    command=previous_question,
    bg="#1f2937",
    fg="white",
    relief="flat",
    padx=20,
    pady=10
).pack(side="left")

tk.Button(
    navigation,
    text="Next →",
    command=next_question,
    bg="#1f2937",
    fg="white",
    relief="flat",
    padx=20,
    pady=10
).pack(side="right")

tk.Button(
    root,
    text="Save JSON",
    command=save_json,
    bg="#2563eb",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    pady=12
).pack(fill="x", padx=30, pady=(5, 5))

status = tk.Label(
    root,
    text="",
    bg="#030712",
    fg="#4ade80"
)
status.pack(pady=(0, 15))

show_question()

root.mainloop()