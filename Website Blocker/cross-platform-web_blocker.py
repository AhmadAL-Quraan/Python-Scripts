import time
import platform
import signal
import sys
from datetime import datetime


class WebsiteBlocker:
    def __init__(
        self, websites: list, start_hour: int = 8, end_hour: int = 16
    ) -> None:
        self.websites = websites
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.redirect = "127.0.0.1"
        self.hosts_path = self.get_hosts_path()

    # ----------------------------
    # OS handling
    # ----------------------------
    def get_hosts_path(self) -> str:
        if platform.system() == "Windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        return "/etc/hosts"

    # ----------------------------
    # Time logic
    # ----------------------------
    def is_working_hours(self) -> bool:
        now = datetime.now()
        return self.start_hour <= now.hour < self.end_hour

    # ----------------------------
    # Blocking logic
    # ----------------------------
    def block_websites(self) -> None:
        try:
            with open(self.hosts_path, "r+") as file:
                content = file.read()

                for site in self.websites:
                    entry = f"{self.redirect} {site}"
                    if entry not in content:
                        file.write(entry + "\n")

        except PermissionError:
            print("❌ Please run the script as administrator/root")
            sys.exit(1)

    # ----------------------------
    # Unblocking logic
    # ----------------------------
    def unblock_websites(self) -> None:
        with open(self.hosts_path, "r+") as file:
            lines = file.readlines()
            file.seek(0)

            for line in lines:
                if not any(site in line for site in self.websites):
                    file.write(line)

            file.truncate()

    # ----------------------------
    # Cleanup on exit
    # ----------------------------
    def cleanup(self, signum=None, frame=None) -> None:
        print("\n🧹 Cleaning up hosts file...")
        self.unblock_websites()
        sys.exit(0)

    # ----------------------------
    # Main loop
    # ----------------------------
    def run(self) -> None:
        print("🚀 Website Blocker running...")

        signal.signal(signal.SIGINT, self.cleanup)

        last_state = None  # Track previous state

        while True:
            current_state = self.is_working_hours()

            # Only act if state changed
            if current_state != last_state:
                if current_state:
                    print("🔒 Blocking websites...")
                    self.block_websites()
                else:
                    print("🔓 Unblocking websites...")
                    print(
                        "⏰ Outside of working hours. Websites are accessible."
                    )
                    self.unblock_websites()

                last_state = current_state  # update state

            time.sleep(30)  # smaller interval is fine now


# ----------------------------
# User input for websites
# ----------------------------
def get_user_websites() -> list:
    options = {
        "1": "facebook.com",
        "2": "youtube.com",
        "3": "instagram.com",
        "4": "twitter.com",
        "5": "gmail.com",
        "6": "\033[33mCustom: Enter your own domains\033[0m",
    }

    print("- Select websites to block (comma separated):")
    for key, value in options.items():
        print(f"{key}) {value}")

    print()
    selected = []
    choices = input("Your choice: ").split(",")
    # Process selected options
    for choice in choices:
        choice = choice.strip()
        if choice in options and choice != "6":
            selected.append(options[choice])
            selected.append("www." + options[choice])
        elif choice == "6":
            custom_sites = input("Enter custom domains (comma separated): ")
            for site in custom_sites.split(","):
                site = site.strip()
                if site:
                    selected.append(site)
                    selected.append("www." + site)
        else:
            print(f"\n\033[91mInvalid option: {choice}\n\
Please select from the list.\033[0m")
            return []

    return selected

    return selected


# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":

    print("\n\033[33mRun this script as administrator/root for \
it to work properly.\033[0m\n")

    websites: list = []
    while len(websites) == 0:
        websites = get_user_websites()

    if not websites:
        print("No websites selected. Exiting.")
        sys.exit(0)

    try:
        start = int(input("Enter the starting hour (0-23) for blocking \
(default 8): "))
        end = int(input("Enter the ending hour (0-23) for blocking \
(default 16): "))
    except ValueError:
        print("Invalid input for hours. Using default values (8-16).")
        start, end = 8, 16

    blocker = WebsiteBlocker(websites, start, end)
    blocker.run()
