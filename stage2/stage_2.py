from pymavlink import mavutil

# Connecting to ArduPilot SITL
master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14551"
)

print("Waiting for heartbeat...")
master.wait_heartbeat()

print("Connected!")
print("System ID:", master.target_system)
print("Component ID:", master.target_component)


# Waiting for a position message
msg = master.recv_match(
    type="GLOBAL_POSITION_INT",
    blocking=True
)

# Converting altitude from millimeters to meters
altitude = msg.relative_alt / 1000.0

print("Altitude:", altitude, "m")
