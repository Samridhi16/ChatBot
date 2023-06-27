## CraveWheels ChatBot: Your Ultimate Food Delivery Assistant 🍔🤖
# Welcome to CraveWheels ChatBot, your companion for food delivery services! 🚀

To run this project, please follow the steps below:

## Getting Started

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
   This will create a local copy of the project on your machine.

2. Add the API key in `server.py`:
   Open the `server.py` file and locate the section where the API key needs to be added. It could be a variable or a configuration file depending on the project. Insert your API key in the designated place.

3. Install the required dependencies:
   - Make sure you have Python installed on your system. The project is compatible with Python versions between 3.7 and 3.9.
   - Install the TTS library by running the following command:
     ```
     pip install TTS
     ```
   - Clone the TTS repository by executing the command:
     ```
     git clone https://github.com/coqui-ai/TTS
     ```
   You can refer to the TTS documentation for more details on its usage.

## Building the Executable

1. Open a terminal or command prompt and navigate to the project directory where the `startBot.py`, `client.py`, and `server.py` files are located.

2. Run the following command to build the executable file:
   ```
   pyinstaller --onefile startBot.py
   ```
   This command will package the Python script into a standalone executable file.

3. Locate the generated `startBot.exe` file in the `dist` folder and keep it within the project directory where `server.py` and `client.py` exits.

## Running the Project

1. Double-click on the `startBot.exe` file to run the program.
