from picar import Picarx


def print_options():
    print("Please enter one of the following:")
    print("1: Drive forward")
    print("2: Parallel park")
    print("3: K-turn")
    print("Q: Exit")


def main():
    px = Picarx()
    print_options()

    options = {1: px.forward_demo, 2: px.parallel_park, 3: px.k_turn}
    speed = 0.5

    while True:
        print("Enter your choice:")
        choice = input()

        if choice in ["q", "Q", "exit", "quit"]:
            print("Exiting!")
            break
        elif int(choice) in options.keys():
            print(f"Executing option {choice}!\n")
            options[int(choice)](speed)
        else:
            print("Invalid choice!\n")
            print_options()


if __name__ == "__main__":
    main()
