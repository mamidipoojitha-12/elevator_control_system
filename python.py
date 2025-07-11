class Elevator:
    def __init__(self, min_floor=1, max_floor=10):
        self.current_floor = min_floor
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.up_queue = []
        self.down_queue = []
        self.direction = "up"

    def enqueue(self, floor):
        if not (self.min_floor <= floor <= self.max_floor):
            print(f"Invalid floor: {floor}. Must be between {self.min_floor} and {self.max_floor}.")
            return

        if floor == self.current_floor:
            print(f"Already on floor {floor}.")
            return

        if floor > self.current_floor:
            if floor not in self.up_queue:
                self.up_queue.append(floor)
                self.up_queue.sort()
                print(f"Floor {floor} added to UP queue.")
        else:
            if floor not in self.down_queue:
                self.down_queue.append(floor)
                self.down_queue.sort(reverse=True)
                print(f"Floor {floor} added to DOWN queue.")

    def external_request(self, floor):
        print(f"External request received for Floor {floor}.")
        self.enqueue(floor)

    def move(self, interactive_mode=True):
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
        else:
            if self.down_queue:
                next_floor = self.down_queue.pop(0)
            elif self.up_queue:
                self.direction = "up"
                print("Switching direction to UP.")
                next_floor = self.up_queue.pop(0)
            else:
                print("No requests pending.")
                return False

        print(f"\n---\nCurrent floor: {self.current_floor}, Moving {self.direction.upper()} to Floor {next_floor}")
        self.current_floor = next_floor
        print(f"Arrived at Floor {self.current_floor}.")
        print("Doors opening...")

        if interactive_mode:
            while True:
                response = input("Passengers boarding here? (yes/no): ").strip().lower()
                if response == 'yes':
                    try:
                        new_floor = int(input("Enter requested floor: "))
                        self.enqueue(new_floor)
                    except ValueError:
                        print("Invalid input.")
                elif response == 'no':
                    break
                else:
                    print("Please enter 'yes' or 'no'.")

        print("Doors closing...")
        self.print_queues()
        return True

    def print_queues(self):
        print(f"UP queue: {self.up_queue}")
        print(f"DOWN queue: {self.down_queue}")

    def run_elevator_dynamic(self, interactive_mode=True):
        while True:
            if not self.up_queue and not self.down_queue:
                print("\nNo requests. Waiting for external request...")
                add = input("Add external request now? (yes/no): ").strip().lower()
                if add == 'yes':
                    try:
                        floor = int(input("Enter external requested floor: "))
                        self.external_request(floor)
                    except ValueError:
                        print("Invalid floor number.")
                    continue
                else:
                    print("No more requests. Elevator shutting down.")
                    break

            moved = self.move(interactive_mode)

            # Simulate dynamic external request during elevator run
            add_more = input("New external request while elevator is moving? (yes/no): ").strip().lower()
            if add_more == 'yes':
                try:
                    floor = int(input("Enter external requested floor: "))
                    self.external_request(floor)
                except ValueError:
                    print("Invalid input.")


# ----------- MAIN DRIVER FUNCTION -----------
def main():
    elevator = Elevator(min_floor=1, max_floor=10)

    mode_input = input("Run in interactive mode (ask for boarding at each stop)? (yes/no): ").strip().lower()
    interactive = (mode_input == 'yes')

    # Initial internal requests
    try:
        n = int(input("How many internal floor requests? "))
        for _ in range(n):
            while True:
                try:
                    floor = int(input("Enter internal requested floor: "))
                    elevator.enqueue(floor)
                    break
                except ValueError:
                    print("Invalid input. Enter a floor number.")
    except ValueError:
        print("Invalid number of requests.")

    # Start the elevator with dynamic handling
    elevator.run_elevator_dynamic(interactive_mode=interactive)


if __name__ == "__main__":
    main()
