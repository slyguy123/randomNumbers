import tkinter as tk
from tkinter import ttk, messagebox
import lotteryPickerLogic

def generate_numbers():
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
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate numbers:\n{str(e)}")

def scrape_and_refresh():
    try:
        start_year_val = int(start_year_scale.get())
        lotteryPickerLogic.scrape_and_save(start_year=start_year_val)
        messagebox.showinfo("Scrape Complete", f"Data scraped from {start_year_val} to current year.")
        generate_numbers()
    except Exception as e:
        messagebox.showerror("Error", f"Scraping failed:\n{str(e)}")

root = tk.Tk()
root.title("Weighted Lottery Number Picker")

ttk.Label(root, text="🎲 Weighted Lottery Picker", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

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

ttk.Label(root, text="Start Year for Scraping").grid(row=5, column=0, sticky="w")
start_year_scale = tk.Scale(root, from_=2000, to=2024, resolution=1, orient="horizontal")
start_year_scale.set(2020)
start_year_scale.grid(row=5, column=1)

generate_btn = ttk.Button(root, text="Generate Numbers", command=generate_numbers)
generate_btn.grid(row=6, column=0, columnspan=2, pady=5)

scrape_btn = ttk.Button(root, text="Scrape & Refresh Data", command=scrape_and_refresh)
scrape_btn.grid(row=7, column=0, columnspan=2, pady=5)

result_var = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_var, font=("Arial", 12), justify="center")
result_label.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
