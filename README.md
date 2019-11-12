# AI-Project1

Authors: Emanuel Sharma (40056523) and Steven Iacobellis (40063086)

### Deliverable 1

For deliverable 1, the program must allow two human players to play X-Rudder according to the game's official rules.

In the code, you will notice that player objects must be passed an AI object at construction. This AI object controls how the player makes their moves. The term AI is a bit of a misnomer here because we can also pass a HumanPlayer object that allows the user to enter moves manually. For this deliverable, the code assigns both players this HumanPlayer AI object.

To operate the HumanPlayer AI, the user must enter their player's move at every turn. If the user wishes to place down a new piece, they enter the coordinates of that piece as follows:
```
coordX coordY
```
Otherwise, if the user wishes to move a piece, they must enter the coordinates of the piece to move followed by the coordinates of the space to move that piece to. This must all be done on **the same line**. The resulting command is formated as follows:
```
origCoordX origCoordY newCoordX newCoordY
```
Note that the moves entered must respect the official game rules. Otherwise, the program will prompt the user to try again. Also, recognize that X coordinates are letters and that Y coordinates are numbers. Use the CLI graphic to help determine the appropriate input.

Finally, note that we also included minimax AI in this deliverable. We included it because we had already begun working on it at the time of submission. That being said, it isn't complete. Consequently, it's been disabled in the code and should be ignored for the time being.

---

We certify that this submission is the original work of members of the group and meets
the Faculty's Expectations of Originality

Emanuel Sharma 40056523 - 10/16/2019
Steven Iacobellis 40063086 - 10/16/2019
