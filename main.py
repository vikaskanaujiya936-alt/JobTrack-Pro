import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import webbrowser
from datetime import date, datetime

DATA_FILE = "jobs.json"

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("JobTrack Pro | Job Application Management System")
root.geometry("1250x800")
root.minsize(1100, 700)
root.configure(bg="#f4f7fb")

dark_mode = False

# =========================================================
# VARIABLES
# =========================================================

search_var = tk.StringVar()
filter_var = tk.StringVar(value="All Status")

total_var = tk.StringVar(value="0")
applied_var = tk.StringVar(value="0")
interview_var = tk.StringVar(value="0")
selected_var = tk.StringVar(value="0")
rejected_var = tk.StringVar(value="0")

selection_rate_var = tk.StringVar(value="0%")
rejection_rate_var = tk.StringVar(value="0%")

# =========================================================
# DATA FUNCTIONS
# =========================================================

def load_all_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_all_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def update_dashboard():
    data = load_all_data()

    total = len(data)
    applied = sum(1 for job in data if job.get("status") == "Applied")
    interviews = sum(1 for job in data if job.get("status") == "Interview")
    selected = sum(1 for job in data if job.get("status") == "Selected")
    rejected = sum(1 for job in data if job.get("status") == "Rejected")

    total_var.set(str(total))
    applied_var.set(str(applied))
    interview_var.set(str(interviews))
    selected_var.set(str(selected))
    rejected_var.set(str(rejected))

    if total > 0:
        selection_rate_var.set(f"{(selected / total) * 100:.1f}%")
        rejection_rate_var.set(f"{(rejected / total) * 100:.1f}%")
    else:
        selection_rate_var.set("0%")
        rejection_rate_var.set("0%")


def refresh_table():
    for item in table.get_children():
        table.delete(item)

    data = load_all_data()

    search_text = search_var.get().lower().strip()
    selected_status = filter_var.get()

    for job in data:

        company = job.get("company", "")
        role = job.get("role", "")
        status = job.get("status", "")

        searchable = (
            company + " " +
            role + " " +
            job.get("location", "") + " " +
            job.get("notes", "")
        ).lower()

        if search_text and search_text not in searchable:
            continue

        if selected_status != "All Status" and status != selected_status:
            continue

        table.insert(
            "",
            "end",
            values=(
                company,
                role,
                job.get("date", ""),
                status,
                job.get("location", ""),
                job.get("interview_date", ""),
                job.get("hr_contact", "")
            )
        )

    update_dashboard()


# =========================================================
# ADD APPLICATION
# =========================================================

def add_application():

    window = tk.Toplevel(root)
    window.title("Add Job Application")
    window.geometry("560x720")
    window.resizable(False, False)
    window.configure(bg="white")

    tk.Label(
        window,
        text="➕ Add Job Application",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e3a8a"
    ).pack(pady=20)

    form = tk.Frame(window, bg="white")
    form.pack(fill="both", expand=True, padx=45)

    # Company
    tk.Label(
        form,
        text="Company Name *",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    company_entry = tk.Entry(form, font=("Arial", 11))
    company_entry.pack(fill="x", pady=(5, 12))

    # Role
    tk.Label(
        form,
        text="Job Role *",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    role_entry = tk.Entry(form, font=("Arial", 11))
    role_entry.pack(fill="x", pady=(5, 12))

    # Date
    tk.Label(
        form,
        text="Applied Date *",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    date_entry = tk.Entry(form, font=("Arial", 11))
    date_entry.insert(0, str(date.today()))
    date_entry.pack(fill="x", pady=(5, 12))

    # Status
    tk.Label(
        form,
        text="Status *",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    status_combo = ttk.Combobox(
        form,
        values=[
            "Applied",
            "Interview",
            "Selected",
            "Rejected"
        ],
        state="readonly",
        font=("Arial", 10)
    )

    status_combo.current(0)
    status_combo.pack(fill="x", pady=(5, 12))

    # Location
    tk.Label(
        form,
        text="Job Location",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    location_entry = tk.Entry(form, font=("Arial", 11))
    location_entry.pack(fill="x", pady=(5, 12))

    # Interview Date
    tk.Label(
        form,
        text="Interview Date",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    interview_date_entry = tk.Entry(form, font=("Arial", 11))
    interview_date_entry.pack(fill="x", pady=(5, 12))

    # HR Contact
    tk.Label(
        form,
        text="HR Contact",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    hr_entry = tk.Entry(form, font=("Arial", 11))
    hr_entry.pack(fill="x", pady=(5, 12))

    # Link
    tk.Label(
        form,
        text="Job / Company Link",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    link_entry = tk.Entry(form, font=("Arial", 11))
    link_entry.pack(fill="x", pady=(5, 12))

    # Notes
    tk.Label(
        form,
        text="Interview / Application Notes",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    notes_entry = tk.Text(
        form,
        height=4,
        font=("Arial", 10)
    )

    notes_entry.pack(fill="x", pady=(5, 15))

    def save_application():

        company = company_entry.get().strip()
        role = role_entry.get().strip()
        applied_date = date_entry.get().strip()
        status = status_combo.get()
        location = location_entry.get().strip()
        interview_date = interview_date_entry.get().strip()
        hr_contact = hr_entry.get().strip()
        link = link_entry.get().strip()
        notes = notes_entry.get("1.0", "end").strip()

        if not company:
            messagebox.showwarning(
                "Required",
                "Please enter company name."
            )
            return

        if not role:
            messagebox.showwarning(
                "Required",
                "Please enter job role."
            )
            return

        if not applied_date:
            messagebox.showwarning(
                "Required",
                "Please enter applied date."
            )
            return

        data = load_all_data()

        data.append({
            "company": company,
            "role": role,
            "date": applied_date,
            "status": status,
            "location": location,
            "interview_date": interview_date,
            "hr_contact": hr_contact,
            "link": link,
            "notes": notes
        })

        save_all_data(data)

        refresh_table()

        messagebox.showinfo(
            "Success",
            "Job application added successfully!"
        )

        window.destroy()

    tk.Button(
        form,
        text="💾 Save Application",
        command=save_application,
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        padx=25,
        pady=10,
        relief="flat",
        cursor="hand2"
    ).pack(pady=5)


# =========================================================
# GET SELECTED JOB
# =========================================================

def get_selected_job():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select an application first."
        )
        return None

    values = table.item(selected[0], "values")

    return values


# =========================================================
# EDIT APPLICATION
# =========================================================

def edit_application():

    values = get_selected_job()

    if not values:
        return

    window = tk.Toplevel(root)
    window.title("Edit Job Application")
    window.geometry("560x720")
    window.resizable(False, False)
    window.configure(bg="white")

    tk.Label(
        window,
        text="✏️ Edit Job Application",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e3a8a"
    ).pack(pady=20)

    form = tk.Frame(window, bg="white")
    form.pack(fill="both", expand=True, padx=45)

    labels = [
        "Company Name *",
        "Job Role *",
        "Applied Date *",
        "Status *",
        "Job Location",
        "Interview Date",
        "HR Contact",
        "Job / Company Link"
    ]

    # Company
    tk.Label(form, text=labels[0],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    company_entry = tk.Entry(form, font=("Arial", 11))
    company_entry.insert(0, values[0])
    company_entry.pack(fill="x", pady=(5, 12))

    # Role
    tk.Label(form, text=labels[1],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    role_entry = tk.Entry(form, font=("Arial", 11))
    role_entry.insert(0, values[1])
    role_entry.pack(fill="x", pady=(5, 12))

    # Date
    tk.Label(form, text=labels[2],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    date_entry = tk.Entry(form, font=("Arial", 11))
    date_entry.insert(0, values[2])
    date_entry.pack(fill="x", pady=(5, 12))

    # Status
    tk.Label(form, text=labels[3],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    status_combo = ttk.Combobox(
        form,
        values=[
            "Applied",
            "Interview",
            "Selected",
            "Rejected"
        ],
        state="readonly"
    )

    status_combo.set(values[3])
    status_combo.pack(fill="x", pady=(5, 12))

    # Location
    tk.Label(form, text=labels[4],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    location_entry = tk.Entry(form, font=("Arial", 11))
    location_entry.insert(0, values[4])
    location_entry.pack(fill="x", pady=(5, 12))

    # Interview Date
    tk.Label(form, text=labels[5],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    interview_entry = tk.Entry(form, font=("Arial", 11))
    interview_entry.insert(0, values[5])
    interview_entry.pack(fill="x", pady=(5, 12))

    # HR
    tk.Label(form, text=labels[6],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    hr_entry = tk.Entry(form, font=("Arial", 11))
    hr_entry.insert(0, values[6])
    hr_entry.pack(fill="x", pady=(5, 12))

    # Link
    tk.Label(form, text=labels[7],
             font=("Arial", 10, "bold"),
             bg="white").pack(anchor="w")

    link_entry = tk.Entry(form, font=("Arial", 11))
    link_entry.pack(fill="x", pady=(5, 12))

    # Notes
    tk.Label(
        form,
        text="Interview / Application Notes",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w")

    notes_text = tk.Text(
        form,
        height=4,
        font=("Arial", 10)
    )

    notes_text.pack(fill="x", pady=(5, 15))

    data = load_all_data()

    old_company = values[0]
    old_role = values[1]
    old_date = values[2]

    old_job = None

    for job in data:

        if (
            job.get("company") == old_company
            and job.get("role") == old_role
            and job.get("date") == old_date
        ):
            old_job = job
            break

    if old_job:

        link_entry.insert(
            0,
            old_job.get("link", "")
        )

        notes_text.insert(
            "1.0",
            old_job.get("notes", "")
        )

    def update_application():

        company = company_entry.get().strip()
        role = role_entry.get().strip()
        applied_date = date_entry.get().strip()
        status = status_combo.get()
        location = location_entry.get().strip()
        interview_date = interview_entry.get().strip()
        hr_contact = hr_entry.get().strip()
        link = link_entry.get().strip()
        notes = notes_text.get("1.0", "end").strip()

        if not company or not role or not applied_date:

            messagebox.showwarning(
                "Required",
                "Please fill all required fields."
            )

            return

        for job in data:

            if (
                job.get("company") == old_company
                and job.get("role") == old_role
                and job.get("date") == old_date
            ):

                job["company"] = company
                job["role"] = role
                job["date"] = applied_date
                job["status"] = status
                job["location"] = location
                job["interview_date"] = interview_date
                job["hr_contact"] = hr_contact
                job["link"] = link
                job["notes"] = notes

                break

        save_all_data(data)

        refresh_table()

        messagebox.showinfo(
            "Updated",
            "Application updated successfully!"
        )

        window.destroy()

    tk.Button(
        form,
        text="💾 Update Application",
        command=update_application,
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        padx=25,
        pady=10,
        relief="flat",
        cursor="hand2"
    ).pack(pady=5)


# =========================================================
# DELETE
# =========================================================

def delete_application():

    values = get_selected_job()

    if not values:
        return

    confirm = messagebox.askyesno(
        "Delete Application",
        "Are you sure you want to delete this application?"
    )

    if not confirm:
        return

    data = load_all_data()

    new_data = []

    deleted = False

    for job in data:

        if (
            not deleted
            and job.get("company") == values[0]
            and job.get("role") == values[1]
            and job.get("date") == values[2]
        ):
            deleted = True
            continue

        new_data.append(job)

    save_all_data(new_data)

    refresh_table()

    messagebox.showinfo(
        "Deleted",
        "Application deleted successfully!"
    )


# =========================================================
# OPEN JOB LINK
# =========================================================

def open_job_link():

    values = get_selected_job()

    if not values:
        return

    data = load_all_data()

    link = ""

    for job in data:

        if (
            job.get("company") == values[0]
            and job.get("role") == values[1]
            and job.get("date") == values[2]
        ):
            link = job.get("link", "")
            break

    if not link:

        messagebox.showinfo(
            "No Link",
            "No job/company link is saved for this application."
        )

        return

    if not link.startswith(("http://", "https://")):
        link = "https://" + link

    webbrowser.open(link)


# =========================================================
# VIEW DETAILS
# =========================================================

def view_details(event=None):

    values = get_selected_job()

    if not values:
        return

    data = load_all_data()

    selected_job = None

    for job in data:

        if (
            job.get("company") == values[0]
            and job.get("role") == values[1]
            and job.get("date") == values[2]
        ):
            selected_job = job
            break

    if not selected_job:
        return

    window = tk.Toplevel(root)
    window.title("Application Details")
    window.geometry("600x620")
    window.resizable(False, False)
    window.configure(bg="white")

    tk.Label(
        window,
        text="📋 Application Details",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e3a8a"
    ).pack(pady=20)

    details = tk.Frame(window, bg="white")
    details.pack(fill="both", expand=True, padx=40)

    information = [
        ("Company", selected_job.get("company", "")),
        ("Job Role", selected_job.get("role", "")),
        ("Applied Date", selected_job.get("date", "")),
        ("Status", selected_job.get("status", "")),
        ("Location", selected_job.get("location", "")),
        ("Interview Date", selected_job.get("interview_date", "")),
        ("HR Contact", selected_job.get("hr_contact", "")),
        ("Job Link", selected_job.get("link", ""))
    ]

    for label, value in information:

        row = tk.Frame(details, bg="white")
        row.pack(fill="x", pady=6)

        tk.Label(
            row,
            text=label + ":",
            font=("Arial", 10, "bold"),
            bg="white",
            width=16,
            anchor="w"
        ).pack(side="left")

        tk.Label(
            row,
            text=value if value else "-",
            font=("Arial", 10),
            bg="white",
            fg="#334155",
            anchor="w",
            justify="left",
            wraplength=390
        ).pack(side="left", fill="x")

    tk.Label(
        details,
        text="Notes",
        font=("Arial", 10, "bold"),
        bg="white"
    ).pack(anchor="w", pady=(15, 5))

    notes = tk.Text(
        details,
        height=7,
        font=("Arial", 10),
        wrap="word"
    )

    notes.pack(fill="both", expand=True)

    notes.insert(
        "1.0",
        selected_job.get("notes", "") or "No notes added."
    )

    notes.config(state="disabled")


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    data = load_all_data()

    if not data:

        messagebox.showinfo(
            "No Data",
            "There are no applications to export."
        )

        return

    filename = filedialog.asksaveasfilename(
        title="Export Job Applications",
        defaultextension=".csv",
        filetypes=[
            ("CSV Files", "*.csv"),
            ("All Files", "*.*")
        ],
        initialfile="job_applications.csv"
    )

    if not filename:
        return

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Company",
            "Job Role",
            "Applied Date",
            "Status",
            "Location",
            "Interview Date",
            "HR Contact",
            "Job Link",
            "Notes"
        ])

        for job in data:

            writer.writerow([
                job.get("company", ""),
                job.get("role", ""),
                job.get("date", ""),
                job.get("status", ""),
                job.get("location", ""),
                job.get("interview_date", ""),
                job.get("hr_contact", ""),
                job.get("link", ""),
                job.get("notes", "")
            ])

    messagebox.showinfo(
        "Export Complete",
        "Job applications exported successfully!"
    )


# =========================================================
# CLEAR ALL
# =========================================================

def clear_all():

    data = load_all_data()

    if not data:

        messagebox.showinfo(
            "No Data",
            "There are no applications to clear."
        )

        return

    confirm = messagebox.askyesno(
        "Clear All",
        "Are you sure you want to delete ALL applications?"
    )

    if not confirm:
        return

    save_all_data([])

    refresh_table()

    messagebox.showinfo(
        "Cleared",
        "All applications have been removed."
    )


# =========================================================
# SEARCH
# =========================================================

def search_applications(event=None):
    refresh_table()


# =========================================================
# STATISTICS WINDOW
# =========================================================

def show_statistics():

    data = load_all_data()

    total = len(data)

    applied = sum(
        1 for job in data
        if job.get("status") == "Applied"
    )

    interviews = sum(
        1 for job in data
        if job.get("status") == "Interview"
    )

    selected = sum(
        1 for job in data
        if job.get("status") == "Selected"
    )

    rejected = sum(
        1 for job in data
        if job.get("status") == "Rejected"
    )

    window = tk.Toplevel(root)
    window.title("JobTrack Pro Statistics")
    window.geometry("650x600")
    window.resizable(False, False)
    window.configure(bg="#f8fafc")

    tk.Label(
        window,
        text="📊 Application Statistics",
        font=("Arial", 23, "bold"),
        bg="#f8fafc",
        fg="#172554"
    ).pack(pady=25)

    chart_frame = tk.Frame(
        window,
        bg="white",
        bd=1,
        relief="solid"
    )

    chart_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(0, 30)
    )

    statuses = [
        ("Applied", applied, "#2563eb"),
        ("Interview", interviews, "#f59e0b"),
        ("Selected", selected, "#16a34a"),
        ("Rejected", rejected, "#dc2626")
    ]

    max_value = max([item[1] for item in statuses] + [1])

    for status, value, color in statuses:

        row = tk.Frame(
            chart_frame,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=12
        )

        tk.Label(
            row,
            text=status,
            font=("Arial", 11, "bold"),
            bg="white",
            width=12,
            anchor="w"
        ).pack(side="left")

        bar_bg = tk.Frame(
            row,
            bg="#e2e8f0",
            height=25
        )

        bar_bg.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        bar_bg.pack_propagate(False)

        bar_width = int(
            (value / max_value) * 300
        )

        if value > 0:

            bar = tk.Frame(
                bar_bg,
                bg=color,
                width=bar_width
            )

            bar.pack(
                side="left",
                fill="y"
            )

        tk.Label(
            row,
            text=str(value),
            font=("Arial", 11, "bold"),
            bg="white",
            width=5
        ).pack(side="right")

    tk.Label(
        chart_frame,
        text=f"Total Applications: {total}",
        font=("Arial", 13, "bold"),
        bg="white",
        fg="#172554"
    ).pack(pady=(25, 5))

    if total:

        selection = (selected / total) * 100
        rejection = (rejected / total) * 100

    else:

        selection = 0
        rejection = 0

    tk.Label(
        chart_frame,
        text=f"Selection Rate: {selection:.1f}%",
        font=("Arial", 11),
        bg="white",
        fg="#15803d"
    ).pack(pady=3)

    tk.Label(
        chart_frame,
        text=f"Rejection Rate: {rejection:.1f}%",
        font=("Arial", 11),
        bg="white",
        fg="#b91c1c"
    ).pack(pady=3)


# =========================================================
# DARK MODE
# =========================================================

def toggle_dark_mode():

    global dark_mode

    dark_mode = not dark_mode

    if dark_mode:

        root.configure(bg="#0f172a")

        section.configure(bg="#0f172a")
        toolbar.configure(bg="#0f172a")
        buttons.configure(bg="#0f172a")

        section_title.configure(
            bg="#0f172a",
            fg="white"
        )

        search_label.configure(
            bg="#0f172a",
            fg="white"
        )

        filter_label.configure(
            bg="#0f172a",
            fg="white"
        )

        footer.configure(
            bg="#0f172a",
            fg="#94a3b8"
        )

        dark_button.config(
            text="☀️ Light Mode"
        )

    else:

        root.configure(bg="#f4f7fb")

        section.configure(bg="#f4f7fb")
        toolbar.configure(bg="#f4f7fb")
        buttons.configure(bg="#f4f7fb")

        section_title.configure(
            bg="#f4f7fb",
            fg="#111827"
        )

        search_label.configure(
            bg="#f4f7fb",
            fg="#111827"
        )

        filter_label.configure(
            bg="#f4f7fb",
            fg="#111827"
        )

        footer.configure(
            bg="#f4f7fb",
            fg="#64748b"
        )

        dark_button.config(
            text="🌙 Dark Mode"
        )


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg="#172554",
    height=100
)

header.pack(fill="x")

tk.Label(
    header,
    text="💼 JobTrack Pro",
    font=("Arial", 28, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=(15, 0))

tk.Label(
    header,
    text="Professional Job Application Management System",
    font=("Arial", 11),
    bg="#172554",
    fg="#dbeafe"
).pack()


# =========================================================
# DASHBOARD
# =========================================================

dashboard = tk.Frame(
    root,
    bg="#f4f7fb"
)

dashboard.pack(
    fill="x",
    padx=25,
    pady=20
)


def create_card(
    title,
    variable,
    bg_color,
    text_color
):

    card = tk.Frame(
        dashboard,
        bg=bg_color,
        height=100
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 9, "bold"),
        bg=bg_color,
        fg="#475569"
    ).pack(pady=(15, 5))

    tk.Label(
        card,
        textvariable=variable,
        font=("Arial", 26, "bold"),
        bg=bg_color,
        fg=text_color
    ).pack()


create_card(
    "TOTAL APPLICATIONS",
    total_var,
    "#dbeafe",
    "#1d4ed8"
)

create_card(
    "APPLIED",
    applied_var,
    "#ede9fe",
    "#6d28d9"
)

create_card(
    "INTERVIEWS",
    interview_var,
    "#fef3c7",
    "#b45309"
)

create_card(
    "SELECTED",
    selected_var,
    "#dcfce7",
    "#15803d"
)

create_card(
    "REJECTED",
    rejected_var,
    "#fee2e2",
    "#b91c1c"
)


# =========================================================
# TOOLBAR
# =========================================================

toolbar = tk.Frame(
    root,
    bg="#f4f7fb"
)

toolbar.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)

search_label = tk.Label(
    toolbar,
    text="🔍 Search",
    font=("Arial", 10, "bold"),
    bg="#f4f7fb"
)

search_label.pack(side="left")

search_entry = tk.Entry(
    toolbar,
    textvariable=search_var,
    font=("Arial", 10),
    width=28
)

search_entry.pack(
    side="left",
    padx=8
)

search_entry.bind(
    "<KeyRelease>",
    search_applications
)


filter_label = tk.Label(
    toolbar,
    text="Filter:",
    font=("Arial", 10, "bold"),
    bg="#f4f7fb"
)

filter_label.pack(
    side="left",
    padx=(15, 5)
)

filter_combo = ttk.Combobox(
    toolbar,
    textvariable=filter_var,
    values=[
        "All Status",
        "Applied",
        "Interview",
        "Selected",
        "Rejected"
    ],
    state="readonly",
    width=15
)

filter_combo.pack(side="left")

filter_combo.bind(
    "<<ComboboxSelected>>",
    lambda event: refresh_table()
)


# Statistics
tk.Button(
    toolbar,
    text="📊 Statistics",
    command=show_statistics,
    font=("Arial", 10, "bold"),
    bg="#7c3aed",
    fg="white",
    padx=14,
    pady=7,
    relief="flat",
    cursor="hand2"
).pack(side="right", padx=5)


# Dark mode
dark_button = tk.Button(
    toolbar,
    text="🌙 Dark Mode",
    command=toggle_dark_mode,
    font=("Arial", 10, "bold"),
    bg="#334155",
    fg="white",
    padx=14,
    pady=7,
    relief="flat",
    cursor="hand2"
)

dark_button.pack(side="right", padx=5)


# Export
tk.Button(
    toolbar,
    text="📄 Export CSV",
    command=export_csv,
    font=("Arial", 10, "bold"),
    bg="#0f766e",
    fg="white",
    padx=14,
    pady=7,
    relief="flat",
    cursor="hand2"
).pack(side="right", padx=5)


# =========================================================
# TABLE SECTION
# =========================================================

section = tk.Frame(
    root,
    bg="#f4f7fb"
)

section.pack(
    fill="both",
    expand=True,
    padx=30
)

section_title = tk.Label(
    section,
    text="My Job Applications",
    font=("Arial", 19, "bold"),
    bg="#f4f7fb",
    fg="#111827"
)

section_title.pack(
    anchor="w",
    pady=(0, 10)
)


table_container = tk.Frame(
    section,
    bg="white"
)

table_container.pack(
    fill="both",
    expand=True
)


columns = (
    "Company",
    "Job Role",
    "Applied Date",
    "Status",
    "Location",
    "Interview Date",
    "HR Contact"
)

table = ttk.Treeview(
    table_container,
    columns=columns,
    show="headings",
    height=13
)


for col in columns:

    table.heading(
        col,
        text=col
    )


table.column(
    "Company",
    width=170,
    anchor="center"
)

table.column(
    "Job Role",
    width=180,
    anchor="center"
)

table.column(
    "Applied Date",
    width=110,
    anchor="center"
)

table.column(
    "Status",
    width=110,
    anchor="center"
)

table.column(
    "Location",
    width=140,
    anchor="center"
)

table.column(
    "Interview Date",
    width=130,
    anchor="center"
)

table.column(
    "HR Contact",
    width=150,
    anchor="center"
)


vertical_scroll = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=table.yview
)

horizontal_scroll = ttk.Scrollbar(
    table_container,
    orient="horizontal",
    command=table.xview
)

table.configure(
    yscrollcommand=vertical_scroll.set,
    xscrollcommand=horizontal_scroll.set
)

table.pack(
    side="left",
    fill="both",
    expand=True
)

vertical_scroll.pack(
    side="right",
    fill="y"
)

horizontal_scroll.pack(
    side="bottom",
    fill="x"
)


# Double click
table.bind(
    "<Double-1>",
    view_details
)


# =========================================================
# BUTTONS
# =========================================================

buttons = tk.Frame(
    root,
    bg="#f4f7fb"
)

buttons.pack(
    fill="x",
    padx=30,
    pady=15
)


tk.Button(
    buttons,
    text="➕ Add Application",
    command=add_application,
    font=("Arial", 10, "bold"),
    bg="#2563eb",
    fg="white",
    padx=18,
    pady=9,
    relief="flat",
    cursor="hand2"
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="✏️ Edit",
    command=edit_application,
    font=("Arial", 10, "bold"),
    bg="#f59e0b",
    fg="white",
    padx=20,
    pady=9,
    relief="flat",
    cursor="hand2"
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="🗑️ Delete",
    command=delete_application,
    font=("Arial", 10, "bold"),
    bg="#dc2626",
    fg="white",
    padx=18,
    pady=9,
    relief="flat",
    cursor="hand2"
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="🔗 Open Job Link",
    command=open_job_link,
    font=("Arial", 10, "bold"),
    bg="#0891b2",
    fg="white",
    padx=18,
    pady=9,
    relief="flat",
    cursor="hand2"
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="📋 View Details",
    command=view_details,
    font=("Arial", 10, "bold"),
    bg="#6366f1",
    fg="white",
    padx=18,
    pady=9,
    relief="flat",
    cursor="hand2"
).pack(
    side="left",
    padx=4
)


tk.Button(
    buttons,
    text="🧹 Clear All",
    command=clear_all,
    font=("Arial", 10, "bold"),
    bg="#64748b",
    fg="white",
    padx=18,
    pady=9,
    relief="flat",
    cursor="hand2"
).pack(
    side="right",
    padx=4
)


# =========================================================
# FOOTER
# =========================================================

footer = tk.Label(
    root,
    text="JobTrack Pro • Python + Tkinter • Job Application Management System",
    font=("Arial", 9),
    bg="#f4f7fb",
    fg="#64748b"
)

footer.pack(
    pady=(0, 8)
)


# =========================================================
# START APPLICATION
# =========================================================

refresh_table()

root.mainloop()