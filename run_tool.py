import subprocess
import sys
from pathlib import Path

TOOLS = {
    "1": Path("GA_Teaching_Tool/teaching_tool.py"),
    "2": Path("ACO_Teaching_Tool/antsp/app.py"),
    "3": Path("CAPyle_releaseV2/release/main.py")
}

def main():
    while True:
        print("\nSelect a tool to run:")
        print("1. GA Teaching Tool")
        print("2. ACO Ants Tool")
        print("3. CAPyle Tool")
        print("4. Exit")

        choice = input("Choose from the above options: ").strip()
        print(f"You entered: {choice}")

        if choice == "4":
            print("Exiting program.")
            sys.exit(0)

        script = TOOLS.get(choice)

        if not script or not script.exists():
            print("Invalid selection or script not found.")
            continue

        try:
            subprocess.run([sys.executable, str(script)], check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e}")
        except KeyboardInterrupt:
            print("\nExecution interrupted by user. Returning to menu.")
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user. Goodbye!")
        sys.exit(0)
