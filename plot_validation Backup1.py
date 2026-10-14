import pandas as pd
import matplotlib.pyplot as plt

# 1. Load Data
print("Loading CSV files...")
df_legacy = pd.read_csv('Legacy_physics.csv')
df_grpc = pd.read_csv('grpc_physics.csv')

# Standardize columns
df_grpc = df_grpc.rename(columns={'OMNeT_X': 'X', 'OMNeT_Y': 'Y'})

# 2. Prepare Data Aggregations
# Time vs Cars (Count unique vehicles per timestep)
cars_legacy = df_legacy.groupby('Time')['VehicleID'].nunique()
cars_grpc = df_grpc.groupby('Time')['VehicleID'].nunique()

# Time vs Average Speed
speed_legacy = df_legacy.groupby('Time')['Speed'].mean()
speed_grpc = df_grpc.groupby('Time')['Speed'].mean()

# Single Car Speed Profile (Micro-validation)
car_id = 'flow0.0'
car_leg = df_legacy[df_legacy['VehicleID'] == car_id]
car_grpc = df_grpc[df_grpc['VehicleID'] == car_id]

# 3. Build the 2x2 Figure
print("Generating thesis plots...")
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Simulation Validation: Legacy TCP vs Modern gRPC', fontsize=18, fontweight='bold')

# --- Panel 1: Time vs Active Cars ---
axs[0, 0].plot(cars_legacy.index, cars_legacy.values, color='gold', linewidth=5, label='Legacy (Yellow)')
axs[0, 0].plot(cars_grpc.index, cars_grpc.values, color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[0, 0].set_title('1. Network Density: Time vs Active Vehicles')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Total Cars on Map')
axs[0, 0].legend()
axs[0, 0].grid(True, alpha=0.3)

# --- Panel 2: Time vs Average Speed ---
axs[0, 1].plot(speed_legacy.index, speed_legacy.values, color='gold', linewidth=5, label='Legacy (Yellow)')
axs[0, 1].plot(speed_grpc.index, speed_grpc.values, color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[0, 1].set_title('2. Macro Physics: Time vs Average Network Speed')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Average Speed (m/s)')
axs[0, 1].legend()
axs[0, 1].grid(True, alpha=0.3)

# --- Panel 3: Single Car Speed Profile ---
axs[1, 0].plot(car_leg['Time'], car_leg['Speed'], color='gold', linewidth=5, label='Legacy (Yellow)')
axs[1, 0].plot(car_grpc['Time'], car_grpc['Speed'], color='blue', linewidth=2, linestyle='--', label='gRPC (Blue)')
axs[1, 0].set_title(f'3. Micro Physics: {car_id} Speed Profile')
axs[1, 0].set_xlabel('Time (s)')
axs[1, 0].set_ylabel('Speed (m/s)')
axs[1, 0].legend()
axs[1, 0].grid(True, alpha=0.3)

# --- Panel 4: Spatial Trajectory Overlay ---
# Yellow base, semi-transparent blue on top. Overlaps will appear greenish-black.
axs[1, 1].scatter(df_legacy['X'], df_legacy['Y'], color='gold', s=60, label='Legacy (Yellow)', alpha=0.6)
axs[1, 1].scatter(df_grpc['X'], df_grpc['Y'], color='blue', s=20, label='gRPC (Blue)', alpha=0.4)
axs[1, 1].set_title('4. Spatial Coordinates: X vs Y Trajectory Overlay')
axs[1, 1].set_xlabel('X Coordinate (Local)')
axs[1, 1].set_ylabel('Y Coordinate (Local)')
axs[1, 1].legend()
axs[1, 1].grid(True, alpha=0.3)

# 4. Finalize and Save
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to fit main title
plt.savefig('thesis_validation_dashboard.png', dpi=300)
print("Plot successfully saved as 'thesis_validation_dashboard.png'!")