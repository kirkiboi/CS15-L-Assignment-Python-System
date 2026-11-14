from load_wallet import LoadWallet


def get_amount(prompt):
    """Ask for a numeric amount and let the caller handle invalid input"""
    return input(prompt).strip()


def main():
    print("================================")
    print("       CELLPHONE LOAD WALLET")
    print("================================")

    owner = input("Enter name: ").strip()
    mobile = input("Enter mobile number: ").strip()
    network = input("Enter your network (Globe, Smart, DITO): ").strip()

    try:
        starting_balance = get_amount("Enter starting balance: ₱")
        wallet = LoadWallet(owner, mobile, network, starting_balance)
    except ValueError as error:
        print(f"Could not create wallet: {error}")
        return

    print(f"\nWelcome, {wallet.owner_name}!")

    while True:
        print("\n========== MAIN MENU ==========")
        print("1. Top up load")
        print("2. Send load (same network)")
        print("3. Check balance")
        print("4. Send load (different network + fee)")
        print("5. Exit")
        print("===============================")

        choice = input("Choose an option").strip()

        try:
            if choice == "1":
                amount = get_amount("Enter top-up amount: ₱")
                wallet.top_up(amount)

            elif choice == "2":
                recipient = input("Enter recipient mobile number: ").strip()
                recipient_network = input("Enter recipient network: ").strip()
                amount = get_amount("Enter amount to send: ₱")
                wallet.send_load(recipient, recipient_network, amount)

            elif choice == "3":
                wallet.show_balance()

            elif choice == "4":
                recipient = input("Enter recipient mobile number: ").strip()
                recipient_network = input("Enter recipient network: ").strip()
                amount = get_amount("Enter amount to send: ₱")
                wallet.send_with_fee(recipient, recipient_network, amount)

            elif choice == "5":
                print("Thank you for using the Cellphone Load Wallet!")
                break

            else:
                print("Invalid choice. Please select from 1 to 5.")

        except ValueError as error:
            print(f"Invalid input: {error}")


if __name__ == "__main__":
    main()
