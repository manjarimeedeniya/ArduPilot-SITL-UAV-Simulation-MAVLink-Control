from pymavlink import mavutil
import time
import math

# Connect to ArduPilot SITL
master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14551"
)

print("Waiting for heartbeat...")
master.wait_heartbeat()

print("Connected!")
print("System ID:", master.target_system)
print("Component ID:", master.target_component)

# Get current position
msg = master.recv_match(
    type="LOCAL_POSITION_NED",
    blocking=True
)

start_x = msg.x
start_y = msg.y
start_z = msg.z

print("\nStarting position:")
print("X:", start_x)
print("Y:", start_y)
print("Z:", start_z)

# Moving 5 meters in the positive X direction
target_x = start_x + 5.0
target_y = start_y
target_z = start_z

print("\nTarget position:")
print("X:", target_x)
print("Y:", target_y)
print("Z:", target_z)

type_mask = 3576

start_time = time.time()

while True:

    # Sending the position target
    master.mav.set_position_target_local_ned_send(

        int(time.time() * 1000) & 0xFFFFFFFF,

        master.target_system,
        master.target_component,

        mavutil.mavlink.MAV_FRAME_LOCAL_NED,

        type_mask,

        target_x,
        target_y,
        target_z,

        0, 0, 0,

        0, 0, 0,

        0,
        0
    )

    # Reading current position
    msg = master.recv_match(
        type="LOCAL_POSITION_NED",
        blocking=True,
        timeout=0.2
    )

    if msg:

        distance = math.sqrt(
            (msg.x - target_x) ** 2 +
            (msg.y - target_y) ** 2 +
            (msg.z - target_z) ** 2
        )

        print(
            f"Position: X={msg.x:.2f}, "
            f"Y={msg.y:.2f}, "
            f"Z={msg.z:.2f}, "
            f"Distance={distance:.2f} m"
        )

        
        if distance < 0.5:

            print("\nTarget reached!")
            break

    # Safety timeout
    if time.time() - start_time > 30:

        print("\nTimeout!")
        break

    # Continueing sending the target
    time.sleep(0.2)


print("Movement complete.")
