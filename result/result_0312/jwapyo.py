import matplotlib.pyplot as plt

# Reload the data from the files after the execution reset
first_file_path = "first_.txt"
second_file_path = "second_.txt"

# Function to extract X, Y coordinates from file
def extract_coordinates(file_path):
    x_coords = []
    y_coords = []
    with open(file_path, "r") as file:
        for line in file:
            if "X:" in line and "Y:" in line:
                parts = line.strip().split(", ")
                x = float(parts[0].split(": ")[1])
                y = float(parts[1].split(": ")[1])
                x_coords.append(x)
                y_coords.append(y)
    return x_coords, y_coords

# Extract coordinates
x1, y1 = extract_coordinates(first_file_path)
x2, y2 = extract_coordinates(second_file_path)

# Create a figure with two columns: one for the large plot, one for the stacked smaller plots
fig = plt.figure(figsize=(15, 6), dpi=150)

# Define grid for subplots (2 columns, 2 rows, but spanning first column for the big plot)
gs = fig.add_gridspec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])

# Large plot with both paths (occupies left side)
ax1 = fig.add_subplot(gs[:, 0])  # This spans both rows in the left column
ax1.plot(x1, y1, label="Preceding Vehicle Path", color="blue", marker="o", markersize=2, linestyle="-")
ax1.plot(x2, y2, label="Lagging Vehicle Path", color="red", marker="x", markersize=2, linestyle="--")
ax1.set_title("Preceding and Lagging Vehicles Path")
ax1.legend()
ax1.grid(True)

# Preceding vehicle path only (top-right small plot)
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(x1, y1, label="Preceding Vehicle Path", color="blue", marker="o", markersize=2, linestyle="-")
ax2.set_title("Preceding Vehicle Path")
ax2.legend()
ax2.grid(True)

# Lagging vehicle path only (bottom-right small plot)
ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(x2, y2, label="Lagging Vehicle Path", color="red", marker="x", markersize=2, linestyle="--")
ax3.set_title("Lagging Vehicle Path")
ax3.legend()
ax3.grid(True)

# Adjust layout for better spacing
plt.tight_layout()

# Show the plots
plt.show()