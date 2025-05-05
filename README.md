# Cosmic Clash

Download the folder from [GitHub]
 - code: download ZIP
 - extract the ZIP file
 - open the folder in vs code: 
  - ensure you are in the correct directory, it should look like this:
    ```
    Cosmic-Clash
    ├── alien.py
    ├── alien_bullet.py
    ├── alien_group.py
    ├── bullet.py
    ├── game.py
    ├── player.py
    ├── README.md
    └── requirements.txt
    ```
 - run requirements.txt
 - run game.py to start the game
 - ENJOY!

## OBJECTIVE
- Don't let the aliens pass you.
- Protect your side of the screen.
- The player to stay alive longest wins the match.

## HOW TO STAY ALIVE
- You lose 1 life when an alien passes your side.
- Aliens move horizontally across the screen.
- Shoot them to reverse their direction.
- If an alien is hit by a bullet:
  - First and second hit: it reverses direction (horizontal bounce).
  - Third hit: it disappears from the game.

## Game Controls
### Player 1 (Left Player):
- `W` = Move Up
- `S` = Move Down
- `D` = Shoot

### Player 2 (Right Player):
- `UP` = Move Up
- `DOWN` = Move Down
- `LEFT` = Shoot
