import tkinter as tk
from tkinter import ttk, messagebox
import lotteryPickerLogic

def update_filter_state():
    """Toggle rollover filtering in the logic module."""
    lotteryPickerLogic.FILTER_ROLLOVERS = filter_var.get() == 1
    generate_numbers()

def update_top_10_display():
    """Refreshes the top 10 most common numbers display."""
    try:
        data = lotteryPickerLogic.prepare_data()
        top_balls = data["ball_counts"].most_common(10)
        display_text = "Top 10 Most Common Numbers:\n"
        for num, count in top_balls:
            display_text += f"{num}: {count} times\n"
        top10_var.set(display_text.strip())
    except Exception as e:
        top10_var.set(f"Error loading top 10:\n{str(e)}")

def generate_numbers():
    """Generate weighted numbers and update UI."""
    try:
        common_weight = float(common_scale.get())
        rare_weight = float(rare_scale.get())
        ball_count = int(core_count.get())
        star_count_val = int(star_count.get())

        final_balls, final_stars = lotteryPickerLogic.generate_custom_draw(
            common_power=common_weight,
            rare_power=rare_weight,
            core_count=ball_count,
            star_count=star_count_val
        )
        result_var.set(f"Core Numbers: {final_balls}\nLucky Stars: {final_stars}")
        update_top_10_display()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate numbers:\n{str(e)}")

def scrape_and_refresh():
    """Scrape fresh results and regenerate CSV."""
    try:
        start_year_val = int(start_year_scale.get())
        lotteryPickerLogic.scrape_and_save(start_year=start_year_val)
        messagebox.showinfo("Scrape Complete", f"Data scraped from {start_year_val} to current year.")
        generate_numbers()
    except Exception as e:
        messagebox.showerror("Error", f"Scraping failed:\n{str(e)}")

# --- Main Window ---
root = tk.Tk()
root.title("Weighted Lottery Number Picker")

# Title
ttk.Label(root, text="🎲 Weighted Lottery Picker", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

# Weighting controls
ttk.Label(root, text="Common Number Weighting").grid(row=1, column=0, sticky="w")
common_scale = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, orient="horizontal")
common_scale.set(1.5)
common_scale.grid(row=1, column=1)

ttk.Label(root, text="Rare Number Weighting").grid(row=2, column=0, sticky="w")
rare_scale = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1, orient="horizontal")
rare_scale.set(0.5)
rare_scale.grid(row=2, column=1)

ttk.Label(root, text="Core Numbers Count").grid(row=3, column=0, sticky="w")
core_count = tk.Spinbox(root, from_=1, to=5, width=5)
core_count.delete(0, tk.END)
core_count.insert(0, "5")
core_count.grid(row=3, column=1)

ttk.Label(root, text="Lucky Stars Count").grid(row=4, column=0, sticky="w")
star_count = tk.Spinbox(root, from_=1, to=2, width=5)
star_count.delete(0, tk.END)
star_count.insert(0, "2")
star_count.grid(row=4, column=1)

# Start year slider
ttk.Label(root, text="Start Year for Scraping").grid(row=5, column=0, sticky="w")
start_year_scale = tk.Scale(root, from_=2000, to=2025, resolution=1, orient="horizontal")
start_year_scale.set(2020)
start_year_scale.grid(row=5, column=1)

# Checkbox for rollover filter
filter_var = tk.IntVar(value=0)
filter_checkbox = ttk.Checkbutton(root, text="Exclude Rollover Draws", variable=filter_var, command=update_filter_state)
filter_checkbox.grid(row=6, column=0, columnspan=2, pady=5)

# Buttons
generate_btn = ttk.Button(root, text="Generate Numbers", command=generate_numbers)
generate_btn.grid(row=7, column=0, columnspan=2, pady=5)

scrape_btn = ttk.Button(root, text="Scrape & Refresh Data", command=scrape_and_refresh)
scrape_btn.grid(row=8, column=0, columnspan=2, pady=5)

# Results display
result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var, font=("Arial", 12), justify="center")
result_label.grid(row=9, column=0, columnspan=2, pady=10)

# Top 10 display
top10_var = tk.StringVar()
top10_label = ttk.Label(root, textvariable=top10_var, font=("Arial", 10), justify="left")
top10_label.grid(row=10, column=0, columnspan=2, pady=10)

# Run initial generation
try:
    generate_numbers()
except Exception:
    pass

root.mainloop()
