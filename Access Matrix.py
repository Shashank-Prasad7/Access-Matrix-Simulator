import tkinter as tk
from tkinter import ttk, messagebox

class AccessMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Access Matrix Simulator")
        self.root.geometry("950x700")
        self.root.configure(bg="#121212")

        # Style Setup
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#121212", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TCombobox", padding=5, font=("Segoe UI", 10))

        # Title
        title = tk.Label(root, text="Access Matrix Simulation", bg="#121212", fg="#00FFC6", font=("Segoe UI", 20, "bold"))
        title.pack(pady=15)

        # Author credit
        author = tk.Label(root, text="Developed by Shashank", bg="#121212", fg="#FFD369", font=("Segoe UI", 11, "italic"))
        author.pack(pady=(0, 15))

        self.create_input_frame()

    def create_input_frame(self):
        """Initial input section for user and file count."""
        self.input_frame = tk.Frame(self.root, bg="#121212")
        self.input_frame.pack(pady=20)

        tk.Label(self.input_frame, text="Number of Users:", fg="white", bg="#121212", font=("Segoe UI", 11)).grid(row=0, column=0, padx=10, pady=5)
        self.user_entry = ttk.Entry(self.input_frame, width=10)
        self.user_entry.grid(row=0, column=1, padx=10)

        tk.Label(self.input_frame, text="Number of Files:", fg="white", bg="#121212", font=("Segoe UI", 11)).grid(row=0, column=2, padx=10)
        self.file_entry = ttk.Entry(self.input_frame, width=10)
        self.file_entry.grid(row=0, column=3, padx=10)

        ttk.Button(self.input_frame, text="Create Matrix", command=self.create_matrix_ui).grid(row=0, column=4, padx=20)

    def create_matrix_ui(self):
        """Builds the dynamic access matrix UI."""
        try:
            self.users = [f"U{i+1}" for i in range(int(self.user_entry.get()))]
            self.files = [f"F{i+1}" for i in range(int(self.file_entry.get()))]
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for users and files!")
            return

        self.input_frame.pack_forget()  # hide initial section

        self.matrix_frame = tk.Frame(self.root, bg="#121212")
        self.matrix_frame.pack(pady=10)

        tk.Label(self.matrix_frame, text="Enter Access Rights (R, W, X, RW, RWX):",
                 fg="#00FFC6", bg="#121212", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=len(self.files)+1, pady=10)

        # Table headers
        tk.Label(self.matrix_frame, text="User/File", fg="#FFD369", bg="#121212", font=("Segoe UI", 11, "bold")).grid(row=1, column=0, padx=10)
        for j, f in enumerate(self.files):
            tk.Label(self.matrix_frame, text=f, fg="#FFD369", bg="#121212", font=("Segoe UI", 11, "bold")).grid(row=1, column=j+1, padx=10)

        self.entries = {}
        for i, u in enumerate(self.users):
            tk.Label(self.matrix_frame, text=u, fg="#00B4D8", bg="#121212", font=("Segoe UI", 10, "bold")).grid(row=i+2, column=0, padx=5)
            for j, f in enumerate(self.files):
                e = ttk.Entry(self.matrix_frame, width=8)
                e.grid(row=i+2, column=j+1, padx=5, pady=5)
                self.entries[(u, f)] = e

        ttk.Button(self.matrix_frame, text="Save Matrix", command=self.save_matrix).grid(row=len(self.users)+3, column=0, columnspan=len(self.files)+1, pady=15)

    def save_matrix(self):
        """Stores all permission values into a dictionary."""
        self.matrix = {}
        for key, entry in self.entries.items():
            val = entry.get().upper().replace(" ", "")
            self.matrix[key] = val

        messagebox.showinfo("Success", "Access Matrix saved successfully!")
        self.create_access_request_ui()

    def create_access_request_ui(self):
        """Access request testing UI."""
        self.access_frame = tk.Frame(self.root, bg="#121212")
        self.access_frame.pack(pady=30)

        tk.Label(self.access_frame, text="Access Request Simulation", fg="#00FFC6",
                 bg="#121212", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        tk.Label(self.access_frame, text="User:", fg="white", bg="#121212").grid(row=1, column=0, padx=10)
        self.user_box = ttk.Combobox(self.access_frame, values=self.users, width=8)
        self.user_box.grid(row=1, column=1)

        tk.Label(self.access_frame, text="File:", fg="white", bg="#121212").grid(row=1, column=2, padx=10)
        self.file_box = ttk.Combobox(self.access_frame, values=self.files, width=8)
        self.file_box.grid(row=1, column=3)

        tk.Label(self.access_frame, text="Operation:", fg="white", bg="#121212").grid(row=2, column=0, padx=10, pady=10)
        self.op_box = ttk.Combobox(self.access_frame, values=["READ (R)", "WRITE (W)", "EXECUTE (X)"], width=15)
        self.op_box.grid(row=2, column=1)

        ttk.Button(self.access_frame, text="Check Access", command=self.check_access).grid(row=2, column=3, padx=10)

        self.result_label = tk.Label(self.access_frame, text="", font=("Segoe UI", 12, "bold"), bg="#121212")
        self.result_label.grid(row=3, column=0, columnspan=4, pady=15)

    def check_access(self):
        """Verifies access request based on matrix."""
        user = self.user_box.get()
        file = self.file_box.get()
        op = self.op_box.get()

        if not user or not file or not op:
            messagebox.showerror("Error", "Please select all fields!")
            return

        symbol = op[0]  # R/W/X
        permission = self.matrix.get((user, file), "")

        if symbol in permission:
            self.result_label.config(
                text=f"Access GRANTED: {user} can {symbol} {file}",
                fg="#00FF88"
            )
        else:
            self.result_label.config(
                text=f"Access DENIED: {user} cannot {symbol} {file}",
                fg="#FF6B6B"
            )

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = AccessMatrixApp(root)
    root.mainloop()
