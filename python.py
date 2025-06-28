class Elevator:
    def __init__(self, min_floor=1, max_floor=10):
        self.current_floor = min_floor
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.up_queue = []     # Floors requested above current floor
        self.down_queue = []   # Floors requested below current floor
        self.direction = "up"  # Elevator starts going up by default

    def enqueue(self, floor):
        if not (self.min_floor <= floor <= self.max_floor):
            print(f"Invalid floor: {floor}. Request a floor between {self.min_floor} and {self.max_floor}.")
            return

        if floor == self.current_floor:
            print(f"Already on floor {floor}.")
            return

        # Add floor to the correct queue based on direction relative to current floor
        if floor > self.current_floor:
            if floor not in self.up_queue:
                self.up_queue.append(floor)
                self.up_queue.sort()
                print(f"Floor {floor} added to UP queue.")
            else:
                print(f"Floor {floor} already in UP queue.")
        else:
            if floor not in self.down_queue:
                self.down_queue.append(floor)
                self.down_queue.sort(reverse=True)
                print(f"Floor {floor} added to DOWN queue.")
            else:
                print(f"Floor {floor} already in DOWN queue.")

    def move(self):
        if self.direction == "up":
            if self.up_queue:
                next_floor = self.up_queue.pop(0)
            elif self.down_queue:
                self.direction = "down"
                print("Switching direction to DOWN.")
                next_floor = self.down_queue.pop(0)
            else:
                print("No requests pending.")
                return False
        else:  # direction == "down"
            if self.down_queue:
                next_floor = self.down_queue.pop(0)
            elif self.up_queue:
                self.direction = "up"
                print("Switching direction to UP.")
                next_floor = self.up_queue.pop(0)
            else:
                print("No requests pending.")
                return False

        direction_str = "up" if next_floor > self.current_floor else "down"
        print(f"Going {direction_str} from Floor {self.current_floor} to Floor {next_floor}.")
        self.current_floor = next_floor
        print(f"Arrived at Floor {self.current_floor}.")

        print("Doors opening...")

        # Ask if passengers boarding here want to add floor requests
        while True:
            response = input(f"Passengers boarding at Floor {self.current_floor}? (yes/no): ").strip().lower()
            if response == 'yes':
                try:
                    floor_request = int(input("Enter floor requested by passenger: "))
                    self.enqueue(floor_request)
                except ValueError:
                    print("Invalid floor number, try again.")
            elif response == 'no':
                break
            else:
                print("Please answer with 'yes' or 'no'.")

        print("Doors closing...")
        self.print_queues()
        return True

    def print_queues(self):
        print(f"UP queue: {self.up_queue}")
        print(f"DOWN queue: {self.down_queue}")

    def external_request(self, floor):
        print(f"External request for Floor {floor}.")
        self.enqueue(floor)

    def run_elevator(self):
        while self.up_queue or self.down_queue:
            if not self.move():
                break
        print("All requested floors have been serviced.")


# ---- MAIN ----
elevator = Elevator(min_floor=1, max_floor=10)

# Internal requests
n = int(input("How many internal floor requests? "))
for _ in range(n):
    while True:
        try:
            floor = int(input("Enter requested floor: "))
            elevator.enqueue(floor)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

elevator.run_elevator()

# External requests
m = int(input("How many external floor requests? "))
for _ in range(m):
    while True:
        try:
            floor = int(input("Enter external requested floor: "))
            elevator.external_request(floor)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

elevator.run_elevator()
