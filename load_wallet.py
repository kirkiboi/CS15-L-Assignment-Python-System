from decimal import Decimal, InvalidOperation


class LoadWallet:
    """subscriber's prepaid cellphone load wallet."""

    SERVICE_FEE = Decimal("2.00")

    def __init__(self, owner_name, mobile_number, network, starting_balance):
        self.owner_name = owner_name
        self.mobile_number = mobile_number
        self.network = network.strip().upper()
        self.balance = self._to_money(starting_balance)

        if not owner_name.strip():
            raise ValueError("Owner name cannot be empty.")
        if not mobile_number.strip():
            raise ValueError("Mobile number cannot be empty.")
        if self.balance < 0:
            raise ValueError("Starting balance cannot be negative.")

    @staticmethod
    def _to_money(amount):
        """Convert an amount to Decimal and reject invalid values."""
        try:
            value = Decimal(str(amount)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError):
            raise ValueError("Please enter a valid amount.")
        return value

    def top_up(self, amount):
        """Add load to the wallet."""
        amount = self._to_money(amount)
        if amount <= 0:
            print("Top-up amount must be greater than zero.")
            return False

        self.balance += amount
        print(f"Top-up successful! Added ₱{amount:.2f}.")
        self.show_balance()
        return True

    def send_load(self, recipient_number, recipient_network, amount):
        """Send load to a number on the same network, without a service fee."""
        amount = self._to_money(amount)
        recipient_network = recipient_network.strip().upper()

        if amount <= 0:
            print("Load amount must be greater than zero.")
            return False
        if recipient_network != self.network:
            print("Different network detected. Please use send_with_fee().")
            return False
        if recipient_number == self.mobile_number:
            print("You cannot send load to your own number.")
            return False
        if self.balance < amount:
            print("Insufficient balance.")
            return False

        self.balance -= amount
        print(f"Successfully sent ₱{amount:.2f} load to {recipient_number}.")
        self.show_balance()
        return True

    def show_balance(self):
        """Display wallet owner and current load balance."""
        print("\n--- WALLET BALANCE ---")
        print(f"Owner: {self.owner_name}")
        print(f"Mobile number: {self.mobile_number}")
        print(f"Network: {self.network}")
        print(f"Available balance: ₱{self.balance:.2f}")
        print("----------------------")

    def send_with_fee(self, recipient_number, recipient_network, amount):
        """Send load to another network and include the service fee."""
        amount = self._to_money(amount)
        recipient_network = recipient_network.strip().upper()

        if amount <= 0:
            print("Load amount must be greater than zero.")
            return False
        if recipient_network == self.network:
            print("Recipient is on the same network. Use send_load() instead.")
            return False
        if recipient_number == self.mobile_number:
            print("You cannot send load to your own number.")
            return False

        total_deduction = amount + self.SERVICE_FEE
        if self.balance < total_deduction:
            print(
                f"Insufficient balance. You need ₱{total_deduction:.2f} "
                f"(including the ₱{self.SERVICE_FEE:.2f} service fee)."
            )
            return False

        self.balance -= total_deduction
        print(f"Successfully sent ₱{amount:.2f} load to {recipient_number}.")
        print(f"Service fee: ₱{self.SERVICE_FEE:.2f}")
        print(f"Total deducted: ₱{total_deduction:.2f}")
        self.show_balance()
        return True
