import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import re
import sys
import csv  # For saving/loading results as CSV
import random  # For generating patient ID
from datetime import datetime  # For date formatting

# Import the illness suggestions from the separate module.
from illness_suggestions import illness_suggestions

# Load symptoms mapping.
try:
    with open("symptoms.json", "r", encoding="utf-8") as f:
        symptoms_mapping = json.load(f)
except Exception as e:
    print("Error loading symptoms.json:", e)
    sys.exit(1)


def clean_text(text):
    if isinstance(text, str):
        text = text.replace("Â", "")
        text = text.replace("â‰¤", "≤")
    return text


def get_field(data_dict, *keys, default=""):
    for key in keys:
        if key in data_dict:
            return data_dict[key]
    return default


def format_range(range_obj):
    if isinstance(range_obj, list):
        return "/".join(map(str, range_obj))
    if isinstance(range_obj, dict):
        if "low" in range_obj and "high" in range_obj:
            return f"{range_obj['low']}-{range_obj['high']} {range_obj.get('unit', '')}".strip()
        elif "operator" in range_obj and "value" in range_obj:
            return f"{range_obj['operator']} {range_obj['value']} {range_obj.get('unit', '')}".strip()
        elif "expected" in range_obj:
            return str(range_obj["expected"])
    return str(range_obj)


def is_qualitative(test, patient_info=None):
    if test.get("expectedValues"):
        return True
    value = test.get("value")
    if isinstance(value, dict) and value.get("expectedValues"):
        return True
    if patient_info and "ageSexGroups" in test:
        sex = patient_info.get("sex")
        if sex and isinstance(test["ageSexGroups"].get(sex), dict):
            for group in test["ageSexGroups"].get(sex).values():
                if isinstance(group, dict) and group.get("expectedValues"):
                    return True
    return False


# --- Helper for age/sex-based expected values ---
def get_expected_from_group(group):
    if isinstance(group, dict):
        if group.get("expectedValues"):
            ev = group["expectedValues"]
            return "/".join(ev) if isinstance(ev, list) else str(ev)
        else:
            return group.get("expected", format_range(group))
    return format_range(group)


def get_normal_range(test, patient_info):
    age = patient_info.get("age")
    sex = patient_info.get("sex")
    if is_qualitative(test, patient_info):
        if test.get("expectedValues"):
            ev = test["expectedValues"]
            return "/".join(ev) if isinstance(ev, list) else str(ev)
        value = test.get("value")
        if isinstance(value, dict) and value.get("expectedValues"):
            ev = value["expectedValues"]
            return "/".join(ev) if isinstance(ev, list) else str(ev)
    if "ageSexGroups" in test and isinstance(test["ageSexGroups"], dict):
        age_sex_groups = test["ageSexGroups"]
        if age is not None and sex:
            sex_groups = age_sex_groups.get(sex)
            if isinstance(sex_groups, dict):
                for age_label, group in sex_groups.items():
                    m = re.search(r'\((\d+)(?:-(\d+))?\+?\)', age_label)
                    if m:
                        min_age = int(m.group(1))
                        max_age = m.group(2)
                        if max_age:
                            max_age = int(max_age)
                            if min_age <= age <= max_age:
                                return get_expected_from_group(group)
                        else:
                            if age >= min_age:
                                return get_expected_from_group(group)
                    else:
                        if age_label.strip().lower() == "all ages":
                            return get_expected_from_group(group)
    age_groups = get_field(test, "ageGroups", "age_groups", default=None)
    if isinstance(age_groups, dict) and age is not None:
        for age_label, group in age_groups.items():
            m = re.search(r'\((\d+)-(\d+)\)', age_label)
            if m:
                min_age = int(m.group(1))
                max_age = int(m.group(2))
                if min_age <= age <= max_age:
                    return format_range(group)
    if "expectedValue" in test:
        return clean_text(test["expectedValue"])
    normal_range = get_field(test, "normalRange", "normal_range", default=None)
    if normal_range is not None and normal_range != "":
        if isinstance(normal_range, str):
            return clean_text(normal_range)
        elif isinstance(normal_range, list):
            if age is not None:
                if age < 40:
                    return clean_text(normal_range[0])
                elif age < 60 and len(normal_range) > 1:
                    return clean_text(normal_range[1])
                elif len(normal_range) > 2:
                    return clean_text(normal_range[2])
                else:
                    return clean_text(normal_range[0])
            else:
                return clean_text(normal_range[0])
        elif isinstance(normal_range, dict):
            if "Male" in normal_range and "Female" in normal_range:
                return clean_text(normal_range.get(sex, normal_range.get("Male")))
            else:
                return format_range(normal_range)
        else:
            return clean_text(str(normal_range))
    expected = get_field(test, "expectedValues", "expected_values", default=None)
    if expected:
        return "/".join(expected) if isinstance(expected, list) else clean_text(expected)
    return "N/A"


# --- Helper for unit extraction ---
def extract_unit_from_text(text):
    tokens = text.split()
    for token in reversed(tokens):
        # A token not entirely made up of digits, dot, dash, or slash is likely a unit.
        if token and not re.fullmatch(r'[\d\.\-\/]+', token):
            return token
    return ""


def extract_unit(test, patient_info):
    if is_qualitative(test, patient_info):
        return "N/A"
    if "unit" in test and test["unit"].strip():
        return test["unit"].strip()

    val = get_normal_range(test, patient_info)
    if isinstance(val, str):
        unit = extract_unit_from_text(val)
        if unit:
            return unit

    normal_range = get_field(test, "normalRange", "normal_range", default=None)
    if isinstance(normal_range, str) and normal_range:
        unit = extract_unit_from_text(normal_range)
        if unit:
            return unit
    if "expectedValue" in test:
        ev = str(test["expectedValue"]).strip()
        unit = extract_unit_from_text(ev)
        if unit:
            return unit
    return ""


def generate_patient_id():
    """Generates a patient ID in the format MT-XXXXXX where XXXXXX is a random 6-digit number."""
    return f"MT-{random.randint(0, 999999):06d}"


# Load diagnosis data.
try:
    with open("diagnosis.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print("Error loading JSON:", e)
    sys.exit(1)
except FileNotFoundError as e:
    print("File not found:", e)
    sys.exit(1)


# Global patient info dictionary and patient ID.
patient_info = {"name": "", "age": None, "sex": ""}
patient_id = None

root = tk.Tk()
root.title("Medical Diagnosis Categories, Tests & Symptoms")
root.geometry("1700x900")  # Wider to accommodate three segments

paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True)

# Left pane: Categories & Tests Treeview
frame_left = ttk.Frame(paned, width=400, relief=tk.SUNKEN)
paned.add(frame_left, weight=1)

# Middle pane: Patient Info, Illness Suggestions, and Test Input/Display
frame_right = ttk.Frame(paned, width=650, relief=tk.SUNKEN)
paned.add(frame_right, weight=2)

# Right-most pane: Symptoms Segment
frame_symptoms = ttk.Frame(paned, width=300, relief=tk.SUNKEN)
paned.add(frame_symptoms, weight=1)

# --- Patient Info Section ---
patient_frame = ttk.Frame(frame_right)
patient_frame.pack(fill=tk.X, padx=10, pady=5)

today_str = datetime.today().strftime("%b %d, %Y")
ttk.Label(patient_frame, text="Date:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
ttk.Label(patient_frame, text=today_str).grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

ttk.Label(patient_frame, text="Patient Name:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
patient_name_entry = ttk.Entry(patient_frame, width=30)
patient_name_entry.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(patient_frame, text="Age:").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
patient_age_entry = ttk.Entry(patient_frame, width=10)
patient_age_entry.grid(row=1, column=3, padx=5, pady=2)
patient_age_entry.insert(0, "45")

ttk.Label(patient_frame, text="Sex:").grid(row=1, column=4, padx=5, pady=2, sticky=tk.W)
patient_sex_combo = ttk.Combobox(patient_frame, values=["Male", "Female"], state="readonly", width=10)
patient_sex_combo.grid(row=1, column=5, padx=5, pady=2)
patient_sex_combo.set("Male")

ttk.Label(patient_frame, text="Patient ID:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
patient_id_entry = ttk.Entry(patient_frame, width=30, state="readonly")
patient_id_entry.grid(row=2, column=1, padx=5, pady=2)


def update_patient_info(event=None):
    global patient_info, patient_id
    patient_info["name"] = patient_name_entry.get().strip()
    try:
        patient_info["age"] = int(patient_age_entry.get().strip())
    except ValueError:
        patient_info["age"] = None
    patient_info["sex"] = patient_sex_combo.get().strip()
    # Generate and display a patient ID if a name is entered and no ID is present.
    if patient_info["name"] and (patient_id is None or patient_id_entry.get().strip() == ""):
        patient_id = generate_patient_id()
        patient_id_entry.config(state="normal")
        patient_id_entry.delete(0, tk.END)
        patient_id_entry.insert(0, patient_id)
        patient_id_entry.config(state="readonly")
    if "tree" in globals() and tree.selection():
        show_details(None)


patient_age_entry.bind("<FocusOut>", update_patient_info)
patient_age_entry.bind("<Return>", update_patient_info)
patient_age_entry.bind("<KeyRelease>", update_patient_info)
patient_sex_combo.bind("<<ComboboxSelected>>", update_patient_info)
patient_name_entry.bind("<FocusOut>", update_patient_info)
patient_name_entry.bind("<KeyRelease>", update_patient_info)

# --- Illness Suggestions Section ---
suggest_frame = ttk.Frame(frame_right)
suggest_frame.pack(fill=tk.X, padx=10, pady=5)
ttk.Label(suggest_frame, text="Select Illness:").pack(side=tk.LEFT, padx=(0, 5))
illness_options = list(illness_suggestions.keys())
illness_combo = ttk.Combobox(suggest_frame, values=illness_options, state="readonly", width=70)
illness_combo.pack(side=tk.LEFT)

suggestion_text = tk.Text(frame_right, wrap=tk.WORD, height=10, state="disabled")
suggestion_text.pack(fill=tk.X, padx=10, pady=(5, 10))

detail_text = tk.Text(frame_right, wrap=tk.WORD, height=10, state="disabled")
detail_text.pack(fill=tk.X, padx=10, pady=(0, 10))

# --- Test Result Input/Display Section ---
results_frame = ttk.Frame(frame_right)
results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
input_frame = ttk.Frame(results_frame)
input_frame.pack(fill=tk.X, padx=5, pady=5)

ttk.Label(input_frame, text="EXAM:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
exam_entry = ttk.Entry(input_frame, width=20, state="readonly")
exam_entry.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(input_frame, text="ABBR:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
abbr_entry = ttk.Entry(input_frame, width=20, state="readonly")
abbr_entry.grid(row=0, column=3, padx=5, pady=2)

ttk.Label(input_frame, text="Conventional:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
conv_entry = ttk.Entry(input_frame, width=20)
conv_entry.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(input_frame, text="UNITS:").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
units_entry = ttk.Entry(input_frame, width=20, state="readonly")
units_entry.grid(row=1, column=3, padx=5, pady=2)

range_label = ttk.Label(input_frame, text="RANGE:")
range_label.grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
range_entry = ttk.Entry(input_frame, width=20, state="readonly")
range_entry.grid(row=2, column=1, padx=5, pady=2, columnspan=3, sticky=tk.W)

def validate_conventional_input(proposed):
    if proposed == "":
        return True
    pattern = r'^\d*\.?\d*(/\d*\.?\d*)?$'
    return re.fullmatch(pattern, proposed) is not None

vcmd = (root.register(validate_conventional_input), '%P')
results_dict = {}

def add_result():
    exam = exam_entry.get().strip()
    abbr = abbr_entry.get().strip()
    conv = conv_entry.get().strip()
    units = units_entry.get().strip()
    result_range = range_entry.get().strip()
    if not (exam and conv and units and result_range):
        return
    if exam in results_dict:
        item_id = results_dict[exam]
        results_tree.item(item_id, values=(exam, abbr, conv, units, result_range))
    else:
        item_id = results_tree.insert("", tk.END, values=(exam, abbr, conv, units, result_range))
        results_dict[exam] = item_id

add_button = ttk.Button(input_frame, text="Add Result", command=add_result)
add_button.grid(row=3, column=0, columnspan=4, pady=5)

# Create results_tree with multiple selection allowed.
results_tree = ttk.Treeview(results_frame,
                            columns=("EXAM", "ABBR", "Conventional", "UNITS", "RANGE"),
                            show="headings",
                            selectmode="extended")
results_tree.heading("EXAM", text="EXAM")
results_tree.heading("ABBR", text="ABBR")
results_tree.heading("Conventional", text="Conventional")
results_tree.heading("UNITS", text="UNITS")
results_tree.heading("RANGE", text="RANGE")
results_tree.column("EXAM", width=150, anchor=tk.CENTER)
results_tree.column("ABBR", width=80, anchor=tk.CENTER)
results_tree.column("Conventional", width=100, anchor=tk.CENTER)
results_tree.column("UNITS", width=80, anchor=tk.CENTER)
results_tree.column("RANGE", width=100, anchor=tk.CENTER)
results_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

def delete_results():
    selected_items = results_tree.selection()
    for item in selected_items:
        exam_value = results_tree.item(item, "values")[0]
        results_tree.delete(item)
        if exam_value in results_dict:
            del results_dict[exam_value]

def load_results():
    """Load exam results and patient info from a CSV file and auto-update all fields from the saved file."""
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        title="Open Exam Results CSV"
    )
    if not file_path:
        return

    try:
        with open(file_path, "r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        if not rows:
            messagebox.showerror("Load Results", "The file is empty.")
            return

        # Expected header: Date, Patient Name, ID, Age, Sex, EXAM, ABBR, Conventional, UNITS, RANGE
        header = rows[0]

        # Clear current exam results
        results_tree.delete(*results_tree.get_children())
        results_dict.clear()

        # If there is at least one data row, update patient info from the first row.
        if len(rows) > 1:
            first_row = rows[1]
            if len(first_row) >= 10:
                # Update patient info fields.
                patient_name_entry.delete(0, tk.END)
                patient_name_entry.insert(0, first_row[1])
                patient_age_entry.delete(0, tk.END)
                patient_age_entry.insert(0, first_row[3])
                patient_sex_combo.set(first_row[4])
                patient_id_entry.config(state="normal")
                patient_id_entry.delete(0, tk.END)
                patient_id_entry.insert(0, first_row[2])
                patient_id_entry.config(state="readonly")

        # Insert exam rows (columns 6 to 10)
        for row in rows[1:]:
            if len(row) < 10:
                continue
            exam, abbr, conv, units, range_val = row[5:10]
            item_id = results_tree.insert("", tk.END, values=(exam, abbr, conv, units, range_val))
            results_dict[exam] = item_id

        # Auto-select the first exam result (if available) to update exam fields.
        children = results_tree.get_children()
        if children:
            results_tree.selection_set(children[0])
            on_result_selected(None)

        messagebox.showinfo("Load Results", f"Loaded {len(rows) - 1} exam result(s) successfully.")
    except Exception as e:
        messagebox.showerror("Load Results", f"Error loading file:\n{str(e)}")


# --- Helper for updating entry widgets ---
def update_entry(entry_widget, text, readonly=True):
    entry_widget.config(state="normal")
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, text)
    if readonly:
        entry_widget.config(state="readonly")


def on_result_selected(event):
    """When a result row is selected, auto-fill the exam fields."""
    selected = results_tree.selection()
    if not selected:
        return
    item = selected[0]
    values = results_tree.item(item, "values")
    # Use the update_entry helper to update the fields.
    update_entry(exam_entry, values[0])
    update_entry(abbr_entry, values[1])
    update_entry(conv_entry, values[2], readonly=False)
    update_entry(units_entry, values[3])
    update_entry(range_entry, values[4])

results_tree.bind("<<TreeviewSelect>>", on_result_selected)

# Create a separate frame for the buttons so they appear on the same line.
buttons_frame = ttk.Frame(results_frame)
buttons_frame.pack(fill=tk.X, padx=5, pady=5)

delete_result_btn = ttk.Button(buttons_frame, text="Delete Selected Results", command=delete_results)
delete_result_btn.pack(side=tk.LEFT, padx=5)

load_result_btn = ttk.Button(buttons_frame, text="Load Results", command=load_results)
load_result_btn.pack(side=tk.LEFT, padx=5)


def save_results():
    """Prompt the user for a file name and save the exam results along with patient info to a CSV file.
    Saving is aborted if any patient info field is blank."""
    # Retrieve patient info fields.
    patient_name = patient_name_entry.get().strip()
    patient_age = patient_age_entry.get().strip()
    patient_sex = patient_sex_combo.get().strip()
    patient_id_value = patient_id_entry.get().strip()
    date_str = today_str.strip()  # Date is set automatically.

    # Check that none of the patient info fields are blank.
    if not (patient_name and patient_age and patient_sex and patient_id_value):
        messagebox.showerror("Save Results",
                             "Please ensure Patient Name, Age, Sex, and Patient ID are filled before saving.")
        return

    # Set the default file name as PatientName_ID.csv
    default_filename = f"{patient_name}_{patient_id_value}.csv"
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        initialdir=r"C:\Users\user\PycharmProjects\Blood_Chem\resut",
        initialfile=default_filename,
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        title="Save Exam Results"
    )
    if not file_path:
        return  # User cancelled

    data_to_save = []
    # Header row includes patient info columns.
    header = ["Date", "Patient Name", "ID", "Age", "Sex", "EXAM", "ABBR", "Conventional", "UNITS", "RANGE"]
    data_to_save.append(header)

    for item in results_tree.get_children():
        exam_values = results_tree.item(item, "values")  # (EXAM, ABBR, Conventional, UNITS, RANGE)
        # Prepend the patient info to each row.
        row = [date_str, patient_name, patient_id_value, patient_age, patient_sex] + list(exam_values)
        data_to_save.append(row)

    try:
        with open(file_path, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_save)
        messagebox.showinfo("Save Results", f"Results saved successfully to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Save Results", f"Error saving results:\n{str(e)}")

save_result_btn = ttk.Button(buttons_frame, text="Save Results", command=save_results)
save_result_btn.pack(side=tk.LEFT, padx=5)

# --- Categories & Tests Treeview (Left Pane) ---
tree = ttk.Treeview(frame_left, show="tree")
tree.heading("#0", text="Category/Test")
tree.column("#0", width=230)
tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

DELIMITER = "::"


def populate_treeview():
    for category, cat_data in data.items():
        # Skip keys that are not dictionaries or do not contain a testList.
        if not (isinstance(cat_data, dict) and "testList" in cat_data):
            continue
        tree.insert("", tk.END, iid=category, text=category)
        tests = cat_data.get("testList", {})
        for test_key, test in tests.items():
            test_name = test.get("name", test_key)
            tree.insert(category, tk.END, iid=f"{category}{DELIMITER}{test_key}", text=test_name)


populate_treeview()


def show_details(event):
    detail_text.config(state="normal")
    detail_text.delete("1.0", tk.END)
    selected = tree.selection()
    if not selected:
        detail_text.config(state="disabled")
        return
    item_id = selected[0]
    parent_id = tree.parent(item_id)
    if parent_id == "":
        # Display category details.
        category = item_id
        cat_data = data.get(category, {})
        description = cat_data.get("description", "No description provided.")
        detail_text.insert(tk.END, f"Category: {category}\n")
        detail_text.insert(tk.END, f"Description: {description}\n\n")
        detail_text.insert(tk.END, "Tests:\n")
        for test_key, test in cat_data.get("testList", {}).items():
            test_name = test.get("name", test_key)
            detail_text.insert(tk.END, f"  - {test_name} ({test_key})\n")
        # Clear the exam-related entries.
        update_entry(exam_entry, "")
        update_entry(abbr_entry, "")
        update_entry(units_entry, "")
        update_entry(range_entry, "")
        range_label.config(text="RANGE:")
    else:
        # Display individual test details.
        parts = item_id.split(DELIMITER, 1)
        if len(parts) != 2:
            detail_text.insert(tk.END, "Error parsing test ID.")
            detail_text.config(state="disabled")
            return
        category, test_key = parts[0], parts[1]
        test = data.get(category, {}).get("testList", {}).get(test_key, {})
        test_name = test.get("name", test_key)
        abbreviation = test.get("abbreviation", test_key)
        test_desc = test.get("description", "No description provided.")
        unit = extract_unit(test, patient_info)
        applicable_sex = test.get("applicableSex", [])
        detail_text.insert(tk.END, f"Test: {test_name}\n")
        detail_text.insert(tk.END, f"Abbreviation: {abbreviation}\n")
        detail_text.insert(tk.END, f"Test Code: {test_key}\n")
        detail_text.insert(tk.END, f"Description: {test_desc}\n")
        detail_text.insert(tk.END, f"Unit: {unit}\n")
        if applicable_sex:
            detail_text.insert(tk.END, f"Applicable Sex: {', '.join(applicable_sex)}\n")
        final_result = get_normal_range(test, patient_info)
        if applicable_sex and patient_info.get("sex") and (patient_info["sex"] not in applicable_sex):
            final_result = "Not Applicable for selected sex"
        if is_qualitative(test, patient_info) or test_key == "Cardiac_Risk":
            detail_text.insert(tk.END, f"Value: {final_result}\n")
            range_label.config(text="VALUE:")
            conv_entry.config(validate="none")
        else:
            detail_text.insert(tk.END, f"Normal Range: {final_result}\n")
            range_label.config(text="RANGE:")
            conv_entry.config(validate="key", validatecommand=vcmd)
            conv_entry.delete(0, tk.END)
        update_entry(exam_entry, test_name)
        update_entry(abbr_entry, abbreviation)
        update_entry(units_entry, unit)
        update_entry(range_entry, final_result)
    detail_text.config(state="disabled")


def on_illness_selected(event):
    suggestion_text.config(state="normal")
    suggestion_text.delete("1.0", tk.END)
    illness = illness_combo.get()
    if illness not in illness_suggestions:
        suggestion_text.insert(tk.END, "No suggestion available.")
        suggestion_text.config(state="disabled")
        return
    suggestion = illness_suggestions[illness]
    suggestion_text.insert(tk.END, f"Suggestion for {illness}:\n\n")
    suggestion_text.insert(tk.END, f"{suggestion['description']}\n\n")
    # For Influenza, also include the tests.
    if illness == "Influenza":
        tests = suggestion.get("tests", [])
        if tests:
            tests_list = [f"{t['category']}:{t['test']}" for t in tests]
            tests_str = ", ".join(tests_list)
            suggestion_text.insert(tk.END, f"{illness}\nRecommended Tests: {tests_str}\n")
        else:
            suggestion_text.insert(tk.END, f"{illness}\n")
    else:
        suggestion_text.insert(tk.END, f"{illness}\n")
    suggestion_text.config(state="disabled")


tree.bind("<<TreeviewSelect>>", show_details)
illness_combo.bind("<<ComboboxSelected>>", on_illness_selected)

# --- Symptoms Segment (Right-Most Pane) ---
ttk.Label(frame_symptoms, text="Select Symptom:", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(5, 2))
symptom_options = list(symptoms_mapping.keys())
symptom_combobox = ttk.Combobox(frame_symptoms, values=symptom_options, state="readonly", width=30)
symptom_combobox.pack(anchor="w", padx=5, pady=2)
if symptom_options:
    symptom_combobox.set(symptom_options[0])


def add_symptom():
    symptom = symptom_combobox.get().strip()
    if not symptom:
        return
    # Prevent duplicate entries
    for child in symptoms_tree.get_children():
        if symptoms_tree.item(child, "values")[0] == symptom:
            return
    symptoms_tree.insert("", "end", values=(symptom,))


add_symptom_btn = ttk.Button(frame_symptoms, text="Add Symptom", command=add_symptom)
add_symptom_btn.pack(anchor="w", padx=5, pady=2)

# Create the symptoms treeview with multiple selection allowed.
symptoms_tree = ttk.Treeview(frame_symptoms, columns=("Symptom",), show="headings", selectmode="extended")
symptoms_tree.heading("Symptom", text="Selected Symptoms")
symptoms_tree.column("Symptom", width=50, anchor="w")
symptoms_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Bind frame_symptoms configure event to update treeview height.
def update_treeview_height(event):
    new_height_pixels = event.height * 0.1  # 10% of frame height in pixels
    new_rows = int(new_height_pixels / 100)
    if new_rows < 1:
        new_rows = 1
    symptoms_tree.config(height=new_rows)

frame_symptoms.bind("<Configure>", update_treeview_height)

def delete_symptoms():
    selected_items = symptoms_tree.selection()
    for item in selected_items:
        symptoms_tree.delete(item)

delete_symptom_btn = ttk.Button(frame_symptoms, text="Delete Selected Symptoms", command=delete_symptoms)
delete_symptom_btn.pack(anchor="w", padx=5, pady=2)

diagnosis_text = tk.Text(frame_symptoms, wrap=tk.WORD, height=10, state="disabled")
diagnosis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

def diagnose_symptoms():
    # Gather selected symptoms from the symptoms_tree and tally associated illnesses.
    diag_counts = {}
    for child in symptoms_tree.get_children():
        symptom = symptoms_tree.item(child, "values")[0]
        for illness in symptoms_mapping.get(symptom, []):
            diag_counts[illness] = diag_counts.get(illness, 0) + 1

    diagnosis_text.config(state="normal")
    diagnosis_text.delete("1.0", tk.END)

    if not diag_counts:
        diagnosis_text.insert(tk.END, "No symptoms selected. Please add symptoms first.")
    else:
        # Sort illnesses alphabetically.
        complete_order = sorted(diag_counts.keys())
        diagnosis_text.insert(tk.END, "Suggested Tests Based on Your Symptoms:\n\n")
        for illness in complete_order:
            suggestion = illness_suggestions.get(illness)
            if suggestion:
                tests = suggestion.get("tests", [])
                new_tests = [f"{t['category']}:{t['test']}" for t in tests]
                diagnosis_text.insert(tk.END, f"- {illness}:\n")
                if new_tests:
                    diagnosis_text.insert(tk.END, "    " + ", ".join(new_tests) + "\n\n")
                else:
                    diagnosis_text.insert(tk.END, "\n")
            else:
                diagnosis_text.insert(tk.END, f"- {illness}: No test suggestions available.\n\n")
    diagnosis_text.config(state="disabled")

diagnose_symptoms_btn = ttk.Button(frame_symptoms, text="Diagnose Symptoms", command=diagnose_symptoms)
diagnose_symptoms_btn.pack(anchor="w", padx=5, pady=5)

update_patient_info()
root.mainloop()
