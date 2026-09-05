from pymavlink import mavutil
import time

# Connecting to ArduPilot SITL
master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14551"
)

print("Waiting for heartbeat...")
master.wait_heartbeat()

print("Connected!")
print("System ID:", master.target_system)
print("Component ID:", master.target_component)

# Setting GUIDED mode
master.set_mode("GUIDED")

time.sleep(2)

# Arming the UAV
master.arducopter_arm()

print("Arming...")
master.motors_armed_wait()

print("Vehicle armed!")

# Sending takeoff command
target_altitude = 5.0

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0, 0, 0,
    target_altitude
)

print("Takeoff command sent.")

# Monitoring altitude
while True:

    msg = master.recv_match(
        type="GLOBAL_POSITION_INT",
        blocking=True,
        timeout=1
    )

    if msg:

        altitude = msg.relative_alt / 1000.0

        print(f"Altitude: {altitude:.2f} m")

        if altitude >= target_altitude - 0.2:
            print("Target altitude reached!")
            break

    time.sleep(0.2)
