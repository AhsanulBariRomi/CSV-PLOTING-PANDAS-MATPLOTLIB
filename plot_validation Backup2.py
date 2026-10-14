import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
print("Loading CSV files...")
df_legacy = pd.read_csv('Legacy_physics.csv')
df_grpc = pd.read_csv('grpc_physics.csv')

# Standardize columns (Updating for new columns)
# Here we rename the columns of the newer grpc dataset so they match the legacy data perfectly.
df_grpc = df_grpc.rename(columns={
    'OMNeT_X': 'X', 
    'OMNeT_Y': 'Y', 
    'OMNeT_Z': 'Z', 
    'Type': 'VehicleType'
})

# Apply manual sorting described in README.txt programmatically 
# This ensures that our data frames are consistently ordered in time, and any simultaneous events are ordered by Vehicle ID.
print("Sorting data by Time and VehicleID...")
df_legacy = df_legacy.sort_values(by=['Time', 'VehicleID'], ascending=[True, True]).reset_index(drop=True)
df_grpc = df_grpc.sort_values(by=['Time', 'VehicleID'], ascending=[True, True]).reset_index(drop=True)

# 2. Prepare Data Aggregations

# --- 1. Network Density Aggregation ---
# Calculation: Group the data by 'Time' (every second), and count the number of UNIQUE 'VehicleID's present at that time.
# Meaning: This tells us how many cars are actively driving on the map at any given second.
cars_legacy = df_legacy.groupby('Time')['VehicleID'].nunique()
cars_grpc = df_grpc.groupby('Time')['VehicleID'].nunique()

# --- 2. Macro Speed Aggregation ---
# Calculation: Group the data by 'Time', and calculate the mathematical average (mean) of the 'Speed' column for all vehicles at that specific second.
# Meaning: This shows the general flow of traffic over time. Drops in this metric indicate network-wide traffic jams or slowing down.
speed_legacy = df_legacy.groupby('Time')['Speed'].mean()
speed_grpc = df_grpc.groupby('Time')['Speed'].mean()

# --- 3. Macro Acceleration Aggregation ---
# Calculation: Group the data by 'Time', and calculate the mathematical average (mean) of the 'Acceleration' column.
# Meaning: This reveals network-wide braking (negative values) or accelerating (positive values) trends across the entire map.
accel_legacy = df_legacy.groupby('Time')['Acceleration'].mean()
accel_grpc = df_grpc.groupby('Time')['Acceleration'].mean()

# --- 4. Single Car (Micro) Filtering ---
# Calculation: Filter both dataframes to only keep rows where the 'VehicleID' is exactly 'flow0.0'.
# Meaning: This isolates a single vehicle's complete journey, allowing us to compare the exact physics of one specific car under both architectures.
car_id = 'flow0.0'
car_leg = df_legacy[df_legacy['VehicleID'] == car_id]
car_grpc = df_grpc[df_grpc['VehicleID'] == car_id]

# 3. Build the 3x2 Figure
print("Generating thesis plots...")
fig, axs = plt.subplots(3, 2, figsize=(16, 18))
fig.suptitle('Simulation Validation: Legacy TCP vs Modern gRPC', fontsize=18, fontweight='bold')

# ==========================================
# Panel 1: Time vs Active Cars
# What it means: Verifies if both simulations spawn and despawn vehicles at the exact same rate.
# How it's plotted: X-axis is Time, Y-axis is the count of unique vehicles (from our aggregation).
# ==========================================
axs[0, 0].plot(cars_legacy.index, cars_legacy.values, color='gold', linewidth=5, label='Legacy (Yellow)')
axs[0, 0].plot(cars_grpc.index, cars_grpc.values, color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[0, 0].set_title('1. Traffic Density: Time vs Active Vehicles')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Total Cars on Map')
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.3)

# ==========================================
# Panel 2: Time vs Average Speed
# What it means: Verifies if the overall traffic flow logic remains identical on a macro level.
# How it's plotted: X-axis is Time, Y-axis is the network's average speed (from our aggregation).
# ==========================================
axs[0, 1].plot(speed_legacy.index, speed_legacy.values, color='gold', linewidth=5, label='Legacy (Yellow)')
axs[0, 1].plot(speed_grpc.index, speed_grpc.values, color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[0, 1].set_title('2. Macro Physics: Time vs Average Traffic Speed')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Average Speed (m/s)')
axs[0, 1].legend()
axs[0, 1].grid(True, alpha=0.3)

# ==========================================
# Panel 3: Single Car Speed Profile
# What it means: A micro-level validation. It verifies if an individual car accelerates, cruises, and decelerates identically in both versions.
# How it's plotted: X-axis is Time, Y-axis is the specific speed of 'flow0.0' at that second.
# ==========================================
axs[1, 0].plot(car_leg['Time'], car_leg['Speed'], color='gold', linewidth=5, label='Legacy (Yellow)')
axs[1, 0].plot(car_grpc['Time'], car_grpc['Speed'], color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[1, 0].set_title(f'3. Micro Physics: {car_id} Speed Profile')
axs[1, 0].set_xlabel('Time (s)')
axs[1, 0].set_ylabel('Speed (m/s)')
axs[1, 0].legend()
axs[1, 0].grid(True, alpha=0.3)

# ==========================================
# Panel 4: Spatial Trajectory Overlay
# What it means: Verifies if the vehicles follow the exact same path/roads geographically.
# How it's plotted: A line plot where X-axis is the X coordinate, Y-axis is the Y coordinate. 
# We use semi-transparent colors (alpha) so overlapping paths will blend together visually.
# ==========================================
# Group by vehicle so it draws separate physical trajectory lines instead of a zig-zag mess
first_leg = True
for v_id, grp in df_legacy.groupby('VehicleID'):
    axs[1, 1].plot(grp['X'], grp['Y'], color='gold', linewidth=3, alpha=0.6, label='Legacy (Yellow)' if first_leg else "")
    first_leg = False
first_grpc = True
for v_id, grp in df_grpc.groupby('VehicleID'):
    axs[1, 1].plot(grp['X'], grp['Y'], color='blue', linewidth=1.5, linestyle='--', alpha=0.6, label='gRPC (Blue)' if first_grpc else "")
    first_grpc = False
axs[1, 1].set_title('4. Spatial Coordinates: X vs Y Trajectory Overlay')
axs[1, 1].set_xlabel('X Coordinate (Local)')
axs[1, 1].set_ylabel('Y Coordinate (Local)')
axs[1, 1].legend()
axs[1, 1].grid(True, alpha=0.3)

# ==========================================
# Panel 5: Time vs Average Acceleration
# What it means: A new macro metric. Verifies if network-wide braking/acceleration behaviors are identical.
# How it's plotted: X-axis is Time, Y-axis is the network's average acceleration (from our aggregation).
# ==========================================
axs[2, 0].plot(accel_legacy.index, accel_legacy.values, color='gold', linewidth=5, label='Legacy (Yellow)')
axs[2, 0].plot(accel_grpc.index, accel_grpc.values, color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[2, 0].set_title('5. Macro Physics: Time vs Average Acceleration')
axs[2, 0].set_xlabel('Time (s)')
axs[2, 0].set_ylabel('Average Acceleration (m/s²)')
axs[2, 0].legend()
axs[2, 0].grid(True, alpha=0.3)

# ==========================================
# Panel 6: Single Car Acceleration Profile
# What it means: A new micro metric. It verifies if a single car presses the gas pedal or brake pedal at the exact same moments.
# How it's plotted: X-axis is Time, Y-axis is the specific acceleration of 'flow0.0' at that second.
# ==========================================
axs[2, 1].plot(car_leg['Time'], car_leg['Acceleration'], color='gold', linewidth=5, label='Legacy (Yellow)')
axs[2, 1].plot(car_grpc['Time'], car_grpc['Acceleration'], color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[2, 1].set_title(f'6. Micro Physics: {car_id} Acceleration Profile')
axs[2, 1].set_xlabel('Time (s)')
axs[2, 1].set_ylabel('Acceleration (m/s²)')
axs[2, 1].legend()
axs[2, 1].grid(True, alpha=0.3)

# 4. Finalize and Save
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to fit main title cleanly
plt.savefig('thesis_validation_dashboard.png', dpi=300)
print("Plot successfully saved as 'thesis_validation_dashboard.png'!")