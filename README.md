# KTAU - Kinpos Test Automation Utility

## Overview

This project is a test automation framework for the Kinpos POS Android application. It is built using Python and Appium. The framework provides a structured way to interact with the application's UI, perform actions, and run test scenarios.

The core design is composed of a `Device` class that provides low-level interaction primitives (like clicking and writing) and a `PortalApp` class that inherits from `Device` and implements the high-level business logic specific to the POS application (like performing a sale or a recharge).

## Core Components

This framework is composed of several key Python modules:

### `portal.py`

This is the main application-specific logic file. It defines the `PortalApp` class which encapsulates all the business flows of the POS application.

- **`class PortalApp(Device)`**: Inherits from the base `Device` class and uses its methods to execute complex workflows.
- **Key Methods**:
    - `login(serial, user, password)`: Logs into the application.
    - `sale(amount, tip, ...)`: Performs a direct sale transaction.
    - `recharge(amount, phone, carrier)`: Performs a mobile phone top-up.
    - `pay(contract, number)`: Pays a service bill.
    - `subsidy(...)`: Handles subsidy transactions.
    - `void_txn()`: Voids the last transaction.
    - `close()`: Performs the end-of-day batch closure.

### `device.py`

This file contains the foundational `Device` class, which acts as a generic interface for interacting with any Appium-driven device. It provides robust and reusable low-level methods.

- **`class Device`**: The base class for all device interactions.
- **Key Methods**:
    - `get_element(*, by, value, element, wait_for, timeout)`: A powerful, unified method to wait for and retrieve elements based on different conditions (`presence`, `clickable`, `writable`). It is the primary function for all element interactions.
    - `wait_for_any(outcomes, timeout, poll_interval)`: An intelligent wait method that waits for the first of many possible outcomes to appear on the screen. This is crucial for handling variable results like "Success", "Insufficient Funds", etc.
    - `click(*, by, value, element, timeout)`: Safely clicks an element after ensuring it is clickable.
    - `write_text(*, by, value, element, text, timeout)`: Safely writes text into an element after ensuring it is ready.
    - `swipe_find(by, value, ...)`: Swipes on the screen until a specific element is found.
    - `hide_keyboard()`: Hides the on-screen keyboard.

### `thedriverfactory.py`

This module is responsible for creating and managing Appium and Selenium WebDriver instances.

- **`class DriverFactory`**: A factory that abstracts away the setup and initialization of drivers.
- **Key Methods**:
    - `get_appium()`: Returns a configured Appium driver instance.
    - `get_selenium()`: Returns a configured Selenium Chrome driver instance.

### `loggerman.py`

This module sets up a project-wide structured logger using the `structlog` library for clear and informative console and file-based logging.

### `iso.py`

A utility script for decoding ISO 8583 message bitmaps. This is useful for debugging the low-level financial data exchanged by the POS application.

### `main.py` & `testrun.py`

These files serve as entry points for executing test scenarios. They demonstrate how to initialize the `DriverFactory` and the `PortalApp` to start running tests. `portal.py` also contains a large `if __name__ == "__main__"` block showing a full test run of most of the app's features.

## Setup & Execution

1.  **Ensure Dependencies are Installed**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Start the Appium Server**: Make sure an Appium 2.0 server is running and accessible at `http://127.0.0.1:4723`.
3.  **Configure the Test Run**: Open `portal.py` and review the `if __name__ == "__main__"` block. You can comment or uncomment the method calls (`app.sale`, `app.recharge`, etc.) to select which tests to run.
4.  **Execute the Test**:
    ```bash
    python portal.py
    ```

## Pending Tasks (TODOs)

The following tasks have been marked in the code for future implementation:

- **`loggerman.py`**:
    - Change log levels based on environment (dev/prod).
    - Add a handler for logging output to a file.
- **`main.py`**:
    - Define the main entry point for the application.
- **`portal.py`**:
    - Implement the DCC (Dynamic Currency Conversion) method.
    - Call the DCC method from within the `sale` function if `dcc != ""`.
- **`thedriverfactory.py`**:
    - Add error handling for both Appium and Selenium driver setup.