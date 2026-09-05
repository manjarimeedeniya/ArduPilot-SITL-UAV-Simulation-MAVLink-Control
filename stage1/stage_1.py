from pymavlink import mavutil

# Connecting to ArduPilot SITL through MAVLink
master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14551"
)

print("Waiting for heartbeat...")

# Waiting until ArduPilot sends a heartbeat
master.wait_heartbeat()

print("Connected!")
print("System ID:", master.target_system)
print("Component ID:", master.target_component)
