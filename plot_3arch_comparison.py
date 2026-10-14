import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# 1. LOAD & STANDARDIZE DATA
# ==============================================================================
print("Loading 600s simulation CSV files...")
df_legacy = pd.read_csv('Legacy_physics_600.csv')
df_grpc = pd.read_csv('grpc_physics_600.csv')
df_lib = pd.read_csv('libsumo_physics_600.csv')

# Standardize column names
rename_dict = {
    'OMNeT_X': 'X', 
    'OMNeT_Y': 'Y', 
    'OMNeT_Z': 'Z', 
    'Type': 'VehicleType'
}
df_grpc = df_grpc.rename(columns=rename_dict)
df_lib = df_lib.rename(columns=rename_dict)

# Programmatic Sorting: Time (Ascending) -> VehicleID (A to Z)
print("Sorting data chronologically by Time and VehicleID...")
df_legacy = df_legacy.sort_values(by=['Time', 'VehicleID']).reset_index(drop=True)
df_grpc = df_grpc.sort_values(by=['Time', 'VehicleID']).reset_index(drop=True)
df_lib = df_lib.sort_values(by=['Time', 'VehicleID']).reset_index(drop=True)

# Architecture configurations with your exact 3 colors
ARCHS = [
    {'name': 'TraCI',    'color': '#ffa347', 'df': df_legacy},
    {'name': 'gRPC',     'color': '#47a3ff', 'df': df_grpc},
    {'name': 'Libsumo',  'color': '#47d147', 'df': df_lib}
]

# Reset to clean standard matplotlib style
plt.rcdefaults()

# ==============================================================================
# 2. PREPARE AGGREGATIONS
# ==============================================================================
print("Calculating aggregations for the 3 architectures...")

# Metric 1: Traffic Density
cars_data = [arch['df'].groupby('Time')['VehicleID'].nunique() for arch in ARCHS]

# Metric 2: Average Traffic Speed
speed_data = [arch['df'].groupby('Time')['Speed'].mean() for arch in ARCHS]

# Metric 3 & 6: Single Car Profile (flow0.0)
target_car_id = 'flow0.0'
single_cars = [arch['df'][arch['df']['VehicleID'] == target_car_id] for arch in ARCHS]

# Metric 5: Average Acceleration
accel_data = [arch['df'].groupby('Time')['Acceleration'].mean() for arch in ARCHS]

# ==============================================================================
# 3. GENERATE 6 SEPARATE 1x3 COMPARISON PLOTS (BOLD & DYNAMIC)
# ==============================================================================

# ------------------------------------------------------------------------------
# PLOT 1: Traffic Density (Active Vehicles over Time)
# ------------------------------------------------------------------------------
print("Generating Plot 1: Traffic Density Comparison...")
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
fig.suptitle('Traffic Density: Time vs Active Vehicles', fontsize=16, fontweight='bold')

for i, arch in enumerate(ARCHS):
    axs[i].plot(cars_data[i].index, cars_data[i].values, color=arch['color'], linewidth=2.5, label=arch['name'])
    axs[i].set_title(arch['name'], fontsize=14, fontweight='bold', color=arch['color'])
    axs[i].set_xlabel('Time (s)', fontsize=12)
    if i == 0:
        axs[i].set_ylabel('Total Cars on Map', fontsize=12)
    axs[i].grid(True, alpha=0.3)
    axs[i].legend(loc='lower right', fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('1_traffic_density_comparison.png', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# PLOT 2: Macro Physics: Time vs Average Traffic Speed
# ------------------------------------------------------------------------------
print("Generating Plot 2: Average Traffic Speed Comparison...")
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
fig.suptitle('Macro Physics: Time vs Average Traffic Speed', fontsize=16, fontweight='bold')

for i, arch in enumerate(ARCHS):
    axs[i].plot(speed_data[i].index, speed_data[i].values, color=arch['color'], linewidth=2.5, label=arch['name'])
    axs[i].set_title(arch['name'], fontsize=14, fontweight='bold', color=arch['color'])
    axs[i].set_xlabel('Time (s)', fontsize=12)
    if i == 0:
        axs[i].set_ylabel('Average Speed (m/s)', fontsize=12)
    axs[i].grid(True, alpha=0.3)
    axs[i].legend(loc='lower right', fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('2_macro_speed_comparison.png', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# PLOT 3: Micro Physics: Single Car (flow0.0) Speed Profile
# ------------------------------------------------------------------------------
print("Generating Plot 3: Single Car Speed Profile Comparison...")
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
fig.suptitle(f'Micro Physics: {target_car_id} Speed Profile', fontsize=16, fontweight='bold')

for i, arch in enumerate(ARCHS):
    car = single_cars[i]
    axs[i].plot(car['Time'], car['Speed'], color=arch['color'], linewidth=2.5, label=arch['name'])
    axs[i].set_title(arch['name'], fontsize=14, fontweight='bold', color=arch['color'])
    axs[i].set_xlabel('Time (s)', fontsize=12)
    if i == 0:
        axs[i].set_ylabel('Speed (m/s)', fontsize=12)
    axs[i].grid(True, alpha=0.3)
    axs[i].legend(loc='lower right', fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('3_micro_speed_comparison.png', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# PLOT 4: Spatial Coordinates: Trajectory Overlay (X vs Y)
# ------------------------------------------------------------------------------
print("Generating Plot 4: Spatial Trajectories Comparison...")
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharex=True, sharey=True)
fig.suptitle('Spatial Coordinates: Vehicle Trajectories (X vs Y)', fontsize=16, fontweight='bold')

for i, arch in enumerate(ARCHS):
    for _, grp in arch['df'].groupby('VehicleID'):
        axs[i].plot(grp['X'], grp['Y'], color=arch['color'], alpha=0.5, linewidth=1.5)
    
    axs[i].set_title(arch['name'], fontsize=14, fontweight='bold', color=arch['color'])
    axs[i].set_xlabel('X Coordinate', fontsize=12)
    if i == 0:
        axs[i].set_ylabel('Y Coordinate', fontsize=12)
    axs[i].grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('4_spatial_trajectories_comparison.png', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# PLOT 5: Macro Physics: Time vs Average Acceleration
# ------------------------------------------------------------------------------
print("Generating Plot 5: Average Acceleration Comparison...")
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
fig.suptitle('Macro Physics: Time vs Average Acceleration', fontsize=16, fontweight='bold')

for i, arch in enumerate(ARCHS):
    axs[i].plot(accel_data[i].index, accel_data[i].values, color=arch['color'], linewidth=2.0, label=arch['name'])
    axs[i].set_title(arch['name'], fontsize=14, fontweight='bold', color=arch['color'])
    axs[i].set_xlabel('Time (s)', fontsize=12)
    if i == 0:
        axs[i].set_ylabel('Average Acceleration (m/s²)', fontsize=12)
    axs[i].grid(True, alpha=0.3)
    axs[i].legend(loc='lower right', fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('5_macro_acceleration_comparison.png', dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# PLOT 6: Micro Physics: Single Car (flow0.0) Acceleration Profile
# ------------------------------------------------------------------------------
print("Generating Plot 6: Single Car Acceleration Profile Comparison...")
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
fig.suptitle(f'Micro Physics: {target_car_id} Acceleration Profile', fontsize=16, fontweight='bold')

for i, arch in enumerate(ARCHS):
    car = single_cars[i]
    axs[i].plot(car['Time'], car['Acceleration'], color=arch['color'], linewidth=2.0, label=arch['name'])
    axs[i].set_title(arch['name'], fontsize=14, fontweight='bold', color=arch['color'])
    axs[i].set_xlabel('Time (s)', fontsize=12)
    if i == 0:
        axs[i].set_ylabel('Acceleration (m/s²)', fontsize=12)
    axs[i].grid(True, alpha=0.3)
    axs[i].legend(loc='lower right', fontsize=11)

plt.tight_layout(rect=[0, 0.03, 1, 0.93])
plt.savefig('6_micro_acceleration_comparison.png', dpi=300)
plt.close()

print("\nAll 6 comparison plots successfully generated and saved!")
