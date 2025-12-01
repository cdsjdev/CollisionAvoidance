import airsim
import time
import sys
import threading

# from getch import pause
import image_collection


def runSingleCar(stop_event: threading.Event, id: int):
    client = airsim.CarClient()
    client.confirmConnection()

    vehicle_name = f"Car_{id}"
    pose = airsim.Pose(airsim.Vector3r(68, -20, 0), airsim.Quaternionr(0, 0, 0, 0))

    print(f"Creating {vehicle_name}")
    success = client.simAddVehicle(vehicle_name, "Physxcar", pose)

    if not success:
        print(f"Failed to create {vehicle_name}")
        return

    time.sleep(1)  # wait for other vehicles to be created

    print(f"Driving {vehicle_name}...")
    client.enableApiControl(True, vehicle_name)

    car_controls = airsim.CarControls()
    time.sleep(2.1)
    # go reverse
    car_controls.throttle = -1
    car_controls.is_manual_gear = True
    car_controls.manual_gear = -1
    car_controls.steering = 1
    client.setCarControls(car_controls, vehicle_name)
    time.sleep(2)
    car_controls.steering = 0
    client.setCarControls(car_controls, vehicle_name)
    car_controls.is_manual_gear = False  # change back gear to auto
    car_controls.manual_gear = 0
    time.sleep(3.59)  # let car drive a bit

    try:
        while not stop_event.is_set():
            time.sleep(2)
            pose = client.simGetVehiclePose(vehicle_name)
            # print(f"{vehicle_name}: ")
            # print(pose.position)
    finally:
        client.enableApiControl(False, vehicle_name)


def runMainCar(stop_event: threading.Event):
    # connect to the main car
    client = airsim.CarClient()
    client.confirmConnection()
    client.reset()
    print("Connected")
    client.enableApiControl(True)
    car_controls = airsim.CarControls()

    print("Driving main car...")

    car_controls.throttle = 2
    car_controls.steering = 0
    client.setCarControls(car_controls)

    try:
        while not stop_event.is_set():
            time.sleep(2)
            pose = client.simGetVehiclePose()
            # print("main car: ")
            # print(pose.position)
    finally:
        client.enableApiControl(False)


def wait_for_quit(stop_event: threading.Event):
    try:
        user_input = input("Press q then Enter to stop...\n")
        if user_input.strip().lower() == "q":
            stop_event.set()
    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    num_vehicles = 1
    if len(sys.argv) == 2:
        num_vehicles = int(sys.argv[1])

    print(f"Creating {num_vehicles} vehicles")

    stop_event = threading.Event()
    threads = []

    t = threading.Thread(target=runMainCar, args=(stop_event,), daemon=True)
    threads.append(t)
    t.start()

    # t = threading.Thread(target=image_collection, args=())
    # threads.append(t)
    # t.start()

    for id in range(num_vehicles, 0, -1):
        t = threading.Thread(target=runSingleCar, args=(stop_event, id), daemon=True)
        threads.append(t)
        t.start()

    input_thread = threading.Thread(target=wait_for_quit, args=(stop_event,), daemon=True)
    input_thread.start()

    try:
        while not stop_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        # give workers a moment to observe stop flag
        time.sleep(0.5)
