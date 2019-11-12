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

For deliverable 2, the program must include an AI capable of playing the game using minimax search and a simple heuristic.

Again, our AI was already ready at the time of the last demo. For this demo, we iterated upon it and made some adjustments.

For example, instead of all win states having the same value, we now value win states that are closer to the root more than win states that are deeper within the tree. This resolves a "problem" we were facing earlier in which the AI would ignore moves that were a win in one move in favour of moves that were a win in 3 moves if the later move was found first. Technically, this "problem" would not affect the AI's odds of winning (a forced win is a forced win no matter how many moves it takes). However, we wanted to avoid it anyways because it prolonged games and made the AI seem naive.

Also, we improved upon the alpha beta pruning by reordering the nodes in the minimax tree. Now, instead of exploring moves by iterating over tiles from the top-left to the bottom-right, the AI iterates over tiles in order of proximity to the tile used for the last move. This increases the odds of good moves being found early and should increase the rate of pruning. The standard approach to reordering is to evaluate the heuristic of all children nodes and order according to those values. However, our approach is both simpler and faster. Furthermore, we believe that, for our heuristic, it yields similar results.

Similarly, we hardcoded the AI's first move. This is a pretty standard approach. There is no point in performing a search for the first move if the best first move will be the same every game. Furthermore, determining the best first move with a search depth of 3 or less is unlikely to yield excellent results.

Lastly, we found that searching with a depth of 2 was very fast, but that searching with a depth of 3 was sometimes too slow (slower than 5 seconds). To receive the benefits of a search depth of 3 while respecting the rules of the game, we iterated upon the simple ab pruning search and came up with something more appropriate. Our AI, before expanding every child of the root node of the search tree, checks to see if it is running out of time. If it is, then our AI uses a search depth of 2, which is very efficient. Otherwise, it continues to use the defualt search depth (3).

That's about it. Beyond these improvements, our AI is fairly standard.

One last inclusion for this delivarable is a prompt at the start of the program to select whether each player should be a human or an AI. This is now easier to modify than it was before, when it had to be done in code.

---

We certify that this submission is the original work of members of the group and meets
the Faculty's Expectations of Originality

Emanuel Sharma 40056523 - 10/16/2019
Steven Iacobellis 40063086 - 10/16/2019
