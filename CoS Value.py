import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import random
import time

# Function to fetch creature details
def fetch_creature_details(creature_name):
    url = f"https://www.game.guide/{creature_name}-value-creatures-of-sonaria"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract creature value
        value_element = soup.find('p', class_='elementor-heading-title', string=lambda t: "Value:" in t)
        value = value_element.text.split(":")[-1].strip() if value_element else "N/A"

        # Extract demand
        demand_element = soup.find('p', class_='elementor-heading-title', string=lambda t: "Demand:" in t)
        demand = demand_element.text.split(":")[-1].strip() if demand_element else "N/A"

        # Extract stability
        stability_element = soup.find('p', class_='elementor-heading-title', string=lambda t: "Stability:" in t)
        stability = stability_element.text.split(":")[-1].strip() if stability_element else "N/A"

        # Extract last updated date
        updated_element = soup.find('time', class_='entry-date')
        updated_date = updated_element['datetime'] if updated_element else "Unknown"

        return value, demand, stability, updated_date
    except requests.exceptions.RequestException as e:
        return "Error fetching data", "N/A", "N/A", "Unknown"

# Function to provide trading tips based on combined demand and stability
def generate_trading_tips(demand, stability):
    tips = []
    
    # Combined interpretation of demand and stability
    if "N/A" not in demand:
        try:
            demand_value = int(demand.split("/")[0])
        except ValueError:
            demand_value = 0  # Handle cases where demand is not a valid integer
        
        # Stability interpretation
        stability_value = 0
        if stability == "STABLE":
            stability_value = 3
        elif stability == "FLUCTUATING":
            stability_value = 2
        elif stability == "DECLINING":
            stability_value = 1
        elif stability == "RISING":
            stability_value = 4
        elif stability == "VERY UNSTABLE":
            stability_value = 0

        combined_value = demand_value + stability_value

        # Generate tips based on combined value
        if combined_value >= 10:
            tips.append("The market conditions are excellent! It's a great time to sell for high value.")
        elif 7 <= combined_value < 10:
            tips.append("Market conditions are good. You can expect decent returns.")
        elif 5 <= combined_value < 7:
            tips.append("Market conditions are average. Plan your trades strategically.")
        elif 3 <= combined_value < 5:
            tips.append("The market is not very favorable right now. It’s better to wait or sell cautiously.")
        else:
            tips.append("The market is unfavorable. It's a risky time to trade.")

    return tips if tips else ["No trading tips available."]

# Function to display results in the GUI
def display_results():
    creature_name = entry.get().replace(" ", "-").lower()
    if not creature_name.strip():
        messagebox.showwarning("Input Error", "Please enter a valid creature name.")
        return

    value, demand, stability, updated_date = fetch_creature_details(creature_name)
    value_text.set(f"{value} Mush")
    demand_text.set(f"{demand} Players")
    stability_text.set(stability)

    # Display the last updated date
    updated_date_label.config(text=f"Last updated: {updated_date}")

    tips = generate_trading_tips(demand, stability)
    tips_text.set("\n".join(tips))

    # Update trading tips text in the Text widget
    tips_entry.config(state=tk.NORMAL)  # Enable the widget to modify text
    tips_entry.delete(1.0, tk.END)  # Clear any existing text
    tips_entry.insert(tk.END, "\n".join(tips))  # Insert the new tips
    tips_entry.config(state=tk.DISABLED)  # Disable the widget again

# Function to animate the background
def animate_background():
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    for _ in range(30):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(-50, 50)
        y2 = y1 + random.randint(-50, 50)
        color = f"#{random.randint(50, 100):02x}{random.randint(50, 100):02x}{random.randint(50, 100):02x}"
        canvas.create_line(x1, y1, x2, y2, fill=color, width=1)

    root.after(100, animate_background)

# Create the GUI application
root = tk.Tk()
root.title("Creature Value Fetcher")
root.geometry("800x600")
root.configure(bg="black")

# Background Canvas
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Input Label and Entry
entry_frame = tk.Frame(root, bg="black")
entry_frame.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

entry_label = tk.Label(entry_frame, text="Enter Creature Name:", font=("Arial", 14), fg="white", bg="black")
entry_label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(entry_frame, width=30, font=("Arial", 14))
entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(entry_frame, text="Search", command=display_results, font=("Arial", 14), bg="#4CAF50", fg="white")
search_button.pack(side=tk.LEFT, padx=5)

# Results Frame
results_frame = tk.Frame(root, bg="black")
results_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Value
value_label = tk.Label(results_frame, text="Creature Values:", font=("Arial", 14), fg="white", bg="black")
value_label.grid(row=0, column=0, pady=5, sticky="e")

value_text = tk.StringVar(value="Results will be displayed here.")
value_entry = tk.Entry(results_frame, textvariable=value_text, font=("Arial", 14), state="readonly", readonlybackground="black", fg="white", width=30, borderwidth=0)
value_entry.grid(row=0, column=1, pady=5, sticky="w")

# Demand
demand_label = tk.Label(results_frame, text="Player Demand:", font=("Arial", 14), fg="white", bg="black")
demand_label.grid(row=1, column=0, pady=5, sticky="e")

demand_text = tk.StringVar(value="N/A")
demand_entry = tk.Entry(results_frame, textvariable=demand_text, font=("Arial", 14), state="readonly", readonlybackground="black", fg="white", width=30, borderwidth=0)
demand_entry.grid(row=1, column=1, pady=5, sticky="w")

# Stability
stability_label = tk.Label(results_frame, text="Price Stability:", font=("Arial", 14), fg="white", bg="black")
stability_label.grid(row=2, column=0, pady=5, sticky="e")

stability_text = tk.StringVar(value="N/A")
stability_entry = tk.Entry(results_frame, textvariable=stability_text, font=("Arial", 14), state="readonly", readonlybackground="black", fg="white", width=30, borderwidth=0)
stability_entry.grid(row=2, column=1, pady=5, sticky="w")

# Last Updated Date
updated_date_label = tk.Label(results_frame, text="Last updated: Unknown", font=("Arial", 12), fg="white", bg="black")
updated_date_label.grid(row=3, column=0, columnspan=2, pady=5)

# Trading Tips
tips_label = tk.Label(results_frame, text="Trading Tips:", font=("Arial", 14), fg="white", bg="black")
tips_label.grid(row=4, column=0, pady=5, sticky="e")

tips_text = tk.StringVar(value="N/A")
tips_entry = tk.Text(results_frame, height=2, width=30, font=("Arial", 14), wrap=tk.WORD, bg="black", fg="white", bd=0)
tips_entry.grid(row=4, column=1, pady=5, sticky="w")
tips_entry.insert(tk.END, "N/A")  # Insert initial text
tips_entry.config(state=tk.DISABLED)  # Make it read-only

# Start the animation and GUI loop
animate_background()
root.mainloop()
