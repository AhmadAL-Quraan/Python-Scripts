# Website Blocker


## Overview

This project is a Python-based website blocker that restricts access to selected websites during specified working hours. It modifies the system's hosts file to redirect targeted domains to the local machine, effectively preventing access.

The script supports both Unix-based systems and Windows by dynamically detecting the operating system and selecting the appropriate hosts file.



## Features
* Cross-platform support (Linux, macOS, Windows)
* Time-based website blocking
* Interactive selection of popular websites
* Support for custom user-defined domains
* Automatic cleanup of hosts file on exit
* Error handling for insufficient permissions
* Modular, object-oriented design



## How It Works

The program modifies the system's hosts file by adding entries that redirect selected domains (e.g., facebook.com) to 127.0.0.1. This prevents the browser from reaching the actual website.

During non-working hours, the script restores the hosts file by removing those entries.

This could be very useful for system administrators, parents, or anyone looking to improve productivity by limiting access to distracting websites during certain hours.


![simple-diagram](pictures/class-diagram.png)



## Requirements

Python 3.x
Administrator/root privileges (required to modify the hosts file)


## Usage


1. Run the script

On Linux/macOS:
```bash
sudo python3 web_blocker.py
```

On Windows (run terminal as Administrator):
```bash
python web_blocker.py
```


2. Select websites
You will be prompted to:
* Choose from a list of common websites
* Or enter custom domains


3. Set working hours
Enter:
* Start hour (0–23)
* End hour (0–23)

If invalid input is provided, default values (8–16) will be used.



## Example


![example](pictures/prompt_asking.png)

If you select:
* facebook.com
* youtube.com

The script will add entries like to the hosts file:
```bash
127.0.0.1 facebook.com
127.0.0.1 www.facebook.com
```

## Important Notes
* The script must be run with administrator/root privileges.
* Modifying the hosts file affects system-wide network behavior.
* The program automatically restores the hosts file when it is stopped using Ctrl+C.


## Improvements Over Original Implementation
* Refactored into an object-oriented design
* Added cross-platform compatibility
* Introduced interactive user input
* Improved timing responsiveness
* Added safe cleanup on exit
* Improved error handling and reliability



## Future Improvements
* Command-line arguments support
* Configuration file for persistent settings
* Logging system
* Unit testing


## Fixing 

* Instead of the program print even if nothing changed, the program remembers its state and It only acts when something actually changes.

## License

This project is part of a public repository intended for educational and practical use.
