from pymavlink import mavutil
import time
import math

master = mavutil.mavlink_connection(
    "udp:127.0.0.1:14551"
)

print("Waiting for heartbeat...")
master.wait_heartbeat()

print("Connected!")
print("System ID:", master.target_system)
print("Component ID:", master.target_component)


msg = master.recv_match(
    type="LOCAL_POSITION_NED",
    blocking=True
)

start_x = msg.x
start_y = msg.y
start_z = msg.z


print("\nStarting position:")
print(f"X: {start_x:.2f}")
print(f"Y: {start_y:.2f}")
print(f"Z: {start_z:.2f}")


# Function to move to a position
def go_to_position(target_x, target_y, target_z):

    print("\nMoving to:")
    print(f"X: {target_x:.2f}")
    print(f"Y: {target_y:.2f}")
    print(f"Z: {target_z:.2f}")


    type_mask = 3576

    start_time = time.time()


    while True:

        # Send position target
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


        # Read current position
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
                f"Position: "
                f"X={msg.x:.2f}, "
                f"Y={msg.y:.2f}, "
                f"Z={msg.z:.2f}, "
                f"Distance={distance:.2f} m"
            )


            # Target reached
            if distance < 0.5:

                print("Target reached!")
                break


        # Safety timeout
        if time.time() - start_time > 30:

            print("Timeout!")
            break


        time.sleep(0.2)

# First target:Move 5 meters in +X direction
target1_x = start_x + 5.0
target1_y = start_y
target1_z = start_z

go_to_position(
    target1_x,
    target1_y,
    target1_z
)

# Second target:Move 3 meters in +Y direction
target2_x = target1_x
target2_y = target1_y + 3.0
target2_z = target1_z

go_to_position(
    target2_x,
    target2_y,
    target2_z
)

print("\nAutonomous navigation complete.")
