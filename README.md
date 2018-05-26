# Clu Clu Land: Secrets of Old Clu Clu Land

Clu Clu Land is an original Nintendo game created for the NES and FDS systems, and arcade cabinets. This project is partially a port of the original NES game, partially an updated version with new level layouts, items, and 4-player support.

## Prerequisites

The project requires python 3, and was designed to work with pygame 1.9.3
Though it may work properly in earlier versions of pygame, I have not tested it on any and cannot guarantee proper performance.

## Gameplay

![title screen](https://i.imgur.com/pbme3bf.png)

### STORY

Long long ago, the evil creatures of the sea urchin nation had stolen the treasure of the balloonfish kingdom, burying it in the mysterious and feared world of Clu Clu Land, where it was thought to be lost forever.
However, the heroic balloonfish Bubbles and her brother Gloopy ventured into this strange world to retrieve their kingdom's gold. In this world, turning around was almost an impossibility: They could only turn by hooking their hands onto a nearby post or bouncing off of a wall, using their momentum to change direction. Despite this handicap, Bubbles and Gloopy retrieved the stolen gold and escaped back to their own land.

Almost a decade later, the boss of the sea urchins hatched a plan to steal the gold once more. He brought the stolen treasures to New Clu Clu Land, a world beneath which he had set up his secret base, prepared to personally welcome Bubbles and Gloopy. Despite the efforts of this massive urchin, the balloonfish were successful once more, and the portal to Clu Clu Land was forgotten.

Now, another 15 years later, the portal has been rediscovered, leading to the ruins of Old Clu Clu Land. Though countless lost treasures must still exist in these ruins, the sea urchins have already infiltrated it, and will stop at nothing to claim all the old world's gold for themselves.
Bubbles and Gloopy are joined by Nemo, the top historian on Old Clu Clu Land, and Dizzy, an eccentric balloonfish who seems to be the only fish with the power to reopen the ancient portal.
Nevertheless, this will be their most perilous mission yet. Only with your help can they successfully discover the secrets of Old Clu Clu Land.

### OBJECT OF THE GAME

To complete a level of Secrets of Old Clu Clu Land, you must reveal all of the gold bars hidden in the stage by passing over them. You can see how many gold bars remain in the level in the status bar at the top of the screen, along with the remaining time for the current level and each player's remaining lives.
The gold bars are always hidden in specific patterns, and in the earlier stages these patterns form recognizable images to help you find it. But you'll have to avoid rubber traps, black holes, and enemy urchins to do so!

Your other goal is of course to collect as many points as possible. Points can be earned by collecting gold, killing sea urchins, finding bonus items, and clearing the bonus stage.
In a 1-player game, additional points can be earned by completing stages quickly.
In other games, additional points can be earned by collecting more gold than any other player.

### HOW TO PLAY

When the level starts, you can move your character in any direction.

Once a player starts moving, they will keep moving in that direction until one of the following happens:
   - The level ends.
   - The player loses a life by hitting an urchin, running out of time, or falling into a black hole.
   - The player hits a wall or another player, at which point they bounce off and move in the opposite direction.
   - The player swings around a post.

Rubber traps begin the stage invisible, and only appear when a player moves directly into one. Coming into contact with a rubber trap will send you in the opposite direction. Once a rubber trap is revealed, the posts that it contacts can no longer be grabbed.

Coming into contact with a sea urchin or black hole will cause you to lose a life. This can be prevented by stunning the sea urchins with your electric shock wave attack (each character may have up to 2 shock waves onscreen at a time), or by using a post to swing your way across a black hole.
Once an urchin is stunned, you may defeat it by crushing it against one of the level boundary walls. After a short time, the urchin will respawn at a black hole.

Once you reach stage 22, the game becomes more difficult. Passing over a gold bar that has already been revealed will hide it again (except in the bonus stage).

### DEFAULT CONTROLS

All controls can be changed via the option in the main menu. No two actions can be mapped to the same control, across any of the four players.

```
   - UP:      up key (P1)          numpad 8 (P2)        w key (P3)           i key (P4)
   - DOWN:    down key (P1)        numpad 2 (P2)        s key (P3)           k key (P4)
   - LEFT:    left key (P1)        numpad 4 (P2)        a key (P3)           j key (P4)
   - RIGHT:   right key (P1)       numpad 6 (P2)        d key (P3)           l key (P4)
   - SHOOT:   z key (P1)           numpad 0 (P2)        q key (P3)           u key (P4)
   - PAUSE:   enter key (P1)       numpad enter (P2)    e key (P3)           o key (P4)
```

### ITEMS

![items](https://github.com/chadfraser/CluGame/blob/master/game/resources/sprite_sheets/item.png)

Bonus fruit (apples, bananas, cherries, eggplants, melons, pineapples, strawberries) all award 800 points to the player who collects them.
Bonus bags award 1500 points to the player who collects them.
Bonus clocks temporarily freeze the timer and stop all sea urchins or other players from moving on their own.
Bonus flags award 1 extra life to the player who collects them.
Bonus glasses reveal all hidden items and gold bars in the stage.

### PATTERNS

```
Pink Stage:    HEART      HOUSE      FACE       HUMAN      BUBBLES    KE         TV         KOOPA
Green Stage:   CLOWN      SPADE      MOUSE      EAGLE      RAIN       CAR        MUSHROOM   SKULL
Blue Stage:    SUBMARINE  GLASSES    KOALA      BUTTERFLY  FISH       CLU CLU    CROWN      SWORD+SHIELD
Purple Stage:  HOLE       KEY        RIBBON     H          !?         FROWN      PYTHON     FLIP
Gold Stage:    SPIDER     X          BOX        DIAMOND    INVERTED   BOX+        CRUSHER    KEY+
```
