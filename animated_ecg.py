import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the plot (dark theme like real ECG)
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 4))
ax.set_facecolor('black')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('gray')
ax.spines['left'].set_color('gray')
ax.grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.4)

# Plot settings
x_window = 4 * np.pi  # Show 2 full heartbeats at a time
x_data = []
y_data = []
line, = ax.plot([], [], color='#00ff41', linewidth=2)
peak_point, = ax.plot([], [], 'ro', markersize=8)  # Red dot for R-peak

# Initialize plot limits
ax.set_xlim(0, x_window)
ax.set_ylim(-2, 2)
ax.set_xlabel("Time (s)", color='white')
ax.set_ylabel("Voltage (mV)", color='white')
ax.set_title("🏥 LIVE ECG SIMULATION – Heartbeat: y = sin(x) + sin(3x)/3", color='cyan', fontsize=14)

# Track time and peak detection
t = 0
dt = 0.05  # time step
last_peak_time = -10  # to avoid duplicate peaks

def animate(frame):
    global t, x_data, y_data, last_peak_time
    
    # Generate next point
    y = np.sin(t) + np.sin(3 * t) / 3
    x_data.append(t)
    y_data.append(y)
    
    # Keep only the last "x_window" seconds of data
    while x_data and x_data[0] < t - x_window:
        x_data.pop(0)
        y_data.pop(0)
    
    # Update the main waveform
    line.set_data(x_data, y_data)
    
    # Detect R-peak: local max near expected peak time (every ~2π)
    # Simple heuristic: if y > 1.2 and rising then falling
    is_peak = False
    if len(y_data) > 2:
        if y_data[-2] > y_data[-3] and y_data[-2] > y_data[-1] and y_data[-2] > 1.2:
            if t - last_peak_time > 3:  # avoid double-detection
                is_peak = True
                last_peak_time = t - dt  # peak was at previous point
    
    # Update peak marker
    if is_peak:
        peak_point.set_data([t - dt], [y_data[-2]])
    else:
        peak_point.set_data([], [])
    
    # Shift x-axis to follow time (scrolling effect)
    ax.set_xlim(t - x_window, t)
    
    t += dt
    return line, peak_point

# Create animation
ani = FuncAnimation(
    fig, 
    animate, 
    frames=1000, 
    interval=50,  # milliseconds between frames (~20 FPS)
    blit=True
)

plt.tight_layout()
plt.show()