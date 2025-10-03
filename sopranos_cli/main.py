# The Sopranos CLI Game
# by Jules

def main():
    """Main function for The Sopranos CLI Game."""
    print("Welcome to The Sopranos CLI Game, ayyy!")
    print("You're a new recruit in the Soprano family. You gotta make a name for yourself.")
    print("What's your first move, wiseguy?")

    while True:
        action = input("> ").lower()
        if action == "quit":
            print("Fuggedaboutit! See you next time.")
            break
        else:
            print("I don't know what you're talkin' about. Try 'quit' to exit.")

if __name__ == "__main__":
    main()