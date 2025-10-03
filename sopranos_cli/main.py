# The Sopranos CLI Game
# by Jules

def get_newspaper():
    """Handles the scenario where Tony gets the newspaper."""
    print("\nYou walk down the long, winding driveway in your robe. The birds are chirping.")
    print("You pick up the Star-Ledger. The headlines are all about the usual garbage.")
    print("You see your neighbor, Dr. Cusamano, watering his lawn. He gives you a nervous wave.")
    print("You wave back. Another beautiful day in the neighborhood.")

def go_to_satrialis():
    """Handles the scenario where Tony goes to Satriale's."""
    print("\nYou get in your black Chevy Suburban and drive over to Satriale's Pork Store.")
    print("The smell of cured meats hits you as soon as you walk in. It's a beautiful thing.")
    print("Big Pussy is behind the counter, slicing up some prosciutto.")
    print("'Tony! What can I get for you?' he asks.")
    print("You order up a pound of gabagool, fresh from the case. The best in Jersey.")

def main():
    """Main function for The Sopranos CLI Game."""
    print("It's a beautiful morning in North Caldwell. You're Tony Soprano, and you're standing in your kitchen in your robe.")
    print("What do you want to do?")
    print("1. Get the newspaper from the end of the driveway.")
    print("2. Head to Satriale's for some gabagool.")

    while True:
        choice = input("> ")
        if choice == "1":
            get_newspaper()
            break
        elif choice == "2":
            go_to_satrialis()
            break
        elif choice == "quit":
            print("Fuggedaboutit! See you next time.")
            break
        else:
            print("What, you got gabagool in your ears? Pick 1 or 2.")

if __name__ == "__main__":
    main()