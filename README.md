# CraveWheels ChatBot: Your Ultimate Food Delivery Assistant 🍔🤖
## Welcome to CraveWheels ChatBot, your companion for food delivery services! 🚀

## [Please find the demo link in the repository]- ### https://github.com/Samridhi16/ChatBot/blob/main/ChatBotDemo.mp4 
   ![image](https://github.com/Samridhi16/ChatBot/assets/26019260/ff787a29-9c21-46f5-b91d-3da66ad7a127)

To run this project, please follow the steps below:

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/Samridhi16/ChatBot.git
   ```
   This will create a local copy of the project on your machine.

2. Add the API key in `server.py`:
   Open the `server.py` file and locate the section where the API key for Open AI needs to be added. It will be a variable in the `server.py` file. Insert your API key in the designated place.

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
   You can refer to the TTS documentation (https://tts.readthedocs.io/en/latest/tutorial_for_nervous_beginners.html) for more details on its usage.

## Building the Executable

1. Open a terminal or command prompt and navigate to the project directory where the `startBot.py`, `client.py`, and `server.py` files are located.

2. Run the following command to build the executable file:
   ```
   pyinstaller --onefile startBot.py
   ```
   This command will package the Python script into a standalone executable file.

3. Locate the generated `startBot.exe` file in the `dist` folder and keep it within the project directory where `server.py` and `client.py` exist.
<br>OR<br> 
1. Start the server:
   ```
   python server.py <port>
   ```
   Replace <port> with the desired port number to listen on.

   Start the client:
   ```
   python client.py <port> <client_number>
   ```
   Replace <port> with the same port number used for the server and <client_number> with a unique identifier for the client.
   
## Running the Project

1. Double-click on the `startBot.exe` file to run the program.




