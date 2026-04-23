import threading
import time
import nav_main
import IP.measuringTaskMain as measure

navigation = threading.Thread(target=nav_main.nav, daemon=True)
navigation.start()

while True:
    program = input("What program do you want to run? (1: photogrammetry, 2: image rec, E: exit): ")
    if program == "1":
        measure.main()
    elif program == "2":        # TODO: add image rec program here
        print("Image recognition program not implemented yet :(")
    elif program.lower() == "e":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please enter 1, 2, or E.")

    time.sleep(1)