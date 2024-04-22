# Online Chess App
I have constructed an online chess app using PyGame, Python’s Chess library, and Python's socket library. PyGame is the basis of the Graphical User Interface (GUI) allowing the players to easily make moves and connect to other players. The Python Chess Library verifies proper chess moves. Finally, the socket library handles the actual direct connections from users to a central server as well as verifies the moves it receives before sending the move to the other player.
## Frontend
The front end of Untitled Chess App is made completely out of PyGame. PyGame allowed me to quickly build a nice UI that runs smoothly and do so relatively quickly.
## Backend
The back end is powered by Python’s chess library and a number of custom functions I made. Python’s chess library handles all the legal moves so that I didn’t need to spend countless hours dealing with the weird rules of chess. 
To make the online functionality, I used the Python socket library to handle direct port connection protocols between each player and the central server. The server does two things: 1) Act as a middleman between the players and 2) Makes sure each player is sending valid moves so they can’t just connect and cheat.

## Install
To install and run this project you just need to clone this repo and install required libraries. To install required libraries, run this command: 
`pip install -r requirements.txt`

## Running
### Offline
To run offline you just need to either run `offline.py` or `main.py`; if you run through `main.py`, just click the button that says "Offline Game". Once open, just play chess, you can reset the board state by pressing the reset button in the top right conner of the game window,
### Online
Before you can run the online game, you need to configer the `config.txt` file to set the IP address and port you want to run through. The default IP and port is `127.0.0.1:8086`; this is just your local host with an arbitrary port. You will ***NOT*** be able to play against someone on a seperate computer if you leave the IP and port like this.
Once you have the IP and port configured how you want, you need to run `server.py` first and then run either `online.py` or `main.py` and just clicking the "Online Game" button. When you do this it will auto connect you to the server. It is important to wait until you connect both clients to the server before making your first move. Once both clients are connected you can just play a game of chess and close the window when you're finished.
