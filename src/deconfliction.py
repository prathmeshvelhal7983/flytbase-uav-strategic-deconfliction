import math
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt

# ==============================
# Data Models
# ==============================
Waypoint = Dict[str, float]  # {'x': float, 'y': float, 'z': float, 'time': float}
Mission = Dict[str, List[Waypoint]]  # {'drone_id': str, 'waypoints': List[Waypoint]}

# ==============================
# Functions
# ==============================

def euclidean_distance(p1: Waypoint, p2: Waypoint) -> float:
    """Calculate 3D Euclidean distance between two waypoints."""
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2 + (p1['z'] - p2['z'])**2)

def detect_conflicts(primary: Mission, others: List[Mission], safe_distance: float = 5.0, time_window: float = 1.0) -> List[Tuple[str, str]]:
    """
    Check if primary mission conflicts with other drone missions.
    Returns a list of tuples with conflicting drone IDs and waypoint times.
    """
    conflicts = []
    for other in others:
        for wp_primary in primary['waypoints']:
            for wp_other in other['waypoints']:
                dist = euclidean_distance(wp_primary, wp_other)
                time_diff = abs(wp_primary['time'] - wp_other['time'])
                if dist < safe_distance and time_diff < time_window:
                    conflicts.append((other['drone_id'], wp_primary['time']))
    return conflicts

def plot_missions(primary: Mission, others: List[Mission], conflicts: List[Tuple[str, float]]):
    """Plot 3D missions and mark conflicts."""
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot primary mission
    x = [wp['x'] for wp in primary['waypoints']]
    y = [wp['y'] for wp in primary['waypoints']]
    z = [wp['z'] for wp in primary['waypoints']]
    ax.plot(x, y, z, label=f"Primary: {primary['drone_id']}", color='blue', linewidth=2)

    # Plot other missions
    colors = ['red', 'green', 'orange', 'purple']
    for i, mission in enumerate(others):
        x = [wp['x'] for wp in mission['waypoints']]
        y = [wp['y'] for wp in mission['waypoints']]
        z = [wp['z'] for wp in mission['waypoints']]
        ax.plot(x, y, z, label=f"Drone: {mission['drone_id']}", color=colors[i % len(colors)], linestyle='--')

    # Mark conflicts
    for drone_id, t in conflicts:
        wp = next((wp for wp in primary['waypoints'] if wp['time'] == t), None)
        if wp:
            ax.scatter(wp['x'], wp['y'], wp['z'], color='red', s=100, marker='x', label=f"Conflict at t={t}s")

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('UAV Mission Trajectories')
    ax.legend()
    plt.show()

# ==============================
# Example Usage
# ==============================

if __name__ == "__main__":
    # Primary mission
    primary_mission = {
        'drone_id': 'DroneA',
        'waypoints': [
            {'x': 0, 'y': 0, 'z': 0, 'time': 0},
            {'x': 10, 'y': 10, 'z': 5, 'time': 5},
            {'x': 20, 'y': 20, 'z': 10, 'time': 10},
        ]
    }

    # Other missions
    other_missions = [
        {
            'drone_id': 'DroneB',
            'waypoints': [
                {'x': 5, 'y': 5, 'z': 2, 'time': 5},
                {'x': 15, 'y': 15, 'z': 7, 'time': 10},
            ]
        },
        {
            'drone_id': 'DroneC',
            'waypoints': [
                {'x': 25, 'y': 25, 'z': 12, 'time': 10},
            ]
        }
    ]

    conflicts = detect_conflicts(primary_mission, other_missions)
    if conflicts:
        print("Conflicts detected:", conflicts)
    else:
        print("No conflicts. Mission is CLEAR.")

    plot_missions(primary_mission, other_missions, conflicts)
