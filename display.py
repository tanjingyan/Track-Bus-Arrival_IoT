def display_bus_info(bus_data):
    print("\nBUS ARRIVAL MONITOR\n")

    for bus in bus_data:
        print(
            f"Bus {bus['bus_no']} | "
            f"{bus['arrival1']} | "
            f"{bus['arrival2']} | "
            f"{bus['arrival3']}"
        )