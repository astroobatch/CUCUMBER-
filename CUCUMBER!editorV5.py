import tkinter as tk
import tkinter.filedialog as filedialog

variables = {}

def substitute_vars(text, vars_dict):
    for var in vars_dict:
        text = text.replace(var, str(vars_dict[var]))
    return text

def generateNewWin_window(title="New Window", description=""):
    win = tk.Toplevel(root)
    win.title(title)
    if description:
        tk.Label(win, text=description, padx=20, pady=20).pack()

def run_code():
    code = editor.get("1.0", tk.END).strip().splitlines()
    output_box.delete("1.0", tk.END)
    global variables
    variables = {}
    i = 0
    while i < len(code):
        line = code[i].strip()
        if line == "" or line.startswith("#"):
            i += 1
            continue

        # var assignment
        if line.startswith("var "):
            parts = line[4:].split("=", 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                value = parts[1].strip()
                if value.isdigit():
                    variables[var_name] = int(value)
                else:
                    value = substitute_vars(value, variables)
                    variables[var_name] = value
            i += 1
            continue

        # input command
        if line.startswith("input "):
            parts = line[6:].split(" ", 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                prompt = parts[1].strip()
                output_box.insert(tk.END, prompt + " ")
                output_box.update()
                user_input = simple_input(prompt)
                variables[var_name] = user_input
                output_box.insert(tk.END, user_input + "\n")
            i += 1
            continue

        # if conditions
        if line.startswith("if "):
            condition = line[3:].strip()
            if "==" in condition:
                var_name, val = map(str.strip, condition.split("=="))
                val = substitute_vars(val, variables)
                var_val = str(variables.get(var_name, ""))
                if var_val != val:
                    i += 2  # skip next line
                else:
                    i += 1
            elif "!=" in condition:
                var_name, val = map(str.strip, condition.split("!="))
                val = substitute_vars(val, variables)
                var_val = str(variables.get(var_name, ""))
                if var_val == val:
                    i += 2  # skip next line
                else:
                    i += 1
            else:
                i += 1
            continue

        # type command
        if line.startswith("type "):
            text = line[5:].strip()
            text = substitute_vars(text, variables)
            output_box.insert(tk.END, text + "\n")
            i += 1
            continue

        # generateNewWin command (just "generateNewWin" opens new window)
        if line == "generateNewWin":
            generateNewWin_window(title="New Window", description="")
            i += 1
            continue

        i += 1

def simple_input(prompt):
    popup = tk.Toplevel(root)
    popup.title(prompt)
    tk.Label(popup, text=prompt).pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
    user_var = tk.StringVar()
    entry = tk.Entry(popup, textvariable=user_var)
    entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    entry.focus()

    result = []

    def on_submit():
        result.append(user_var.get())
        popup.destroy()

    submit_btn = tk.Button(popup, text="OK", command=on_submit)
    submit_btn.pack(side=tk.TOP, pady=10)
    popup.transient(root)
    popup.grab_set()
    root.wait_window(popup)
    return result[0] if result else ""

def save_code():
    file_path = filedialog.asksaveasfilename(defaultextension=".cuke",
                                             filetypes=[("CUCUMBER Files", "*.cuke"), ("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(editor.get("1.0", tk.END))

def load_code():
    file_path = filedialog.askopenfilename(filetypes=[("CUCUMBER Files", "*.cuke"), ("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            editor.delete("1.0", tk.END)
            editor.insert("1.0", content)

root = tk.Tk()
root.title("CUCUMBER! Interpreter")

editor_frame = tk.Frame(root)
editor_frame.pack(fill=tk.BOTH, expand=True)

editor_label = tk.Label(editor_frame, text="Write your CUCUMBER! code below:")
editor_label.pack(anchor="w")

editor = tk.Text(editor_frame, height=15, width=80)
editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

run_button = tk.Button(button_frame, text="Run", command=run_code)
run_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = tk.Button(button_frame, text="Save", command=save_code)
save_button.pack(side=tk.LEFT, padx=5, pady=5)

load_button = tk.Button(button_frame, text="Load", command=load_code)
load_button.pack(side=tk.LEFT, padx=5, pady=5)

output_frame = tk.Frame(root)
output_frame.pack(fill=tk.BOTH, expand=True)

output_label = tk.Label(output_frame, text="Output:")
output_label.pack(anchor="w")

output_box = tk.Text(output_frame, height=15, width=80, state=tk.NORMAL)
output_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

root.mainloop()
()
