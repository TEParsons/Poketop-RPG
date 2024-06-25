---
title: Home
---

Pokétop RPG is a tabletop RPG system using the actual in-game stats from Pokémon (Gen I, for now...) games to determine roll modifiers.

# Battling
Just like in the games, battles are turn-based. When you start a battle, you choose a Pokémon to send out, as does your opponent, and the battle begins. Details of the evens in a turn are described below.

#### Choosing moves
Before you do anything else (including determining who goes first), you choose what move you're going to use. Your Pokémon will know up to 4 moves. You can also, instead of using a move, choose to switch out for a different Pokémon in your party, or use an item. 

#### Running
In battles with wild Pokémon, you can choose to run instead of attacking. If you choose this, before the rest of the turn happens, your Pokémon and the opponent both roll d20's and add their Speed modifiers. If your Pokémon has the higher roll, you escape successfully and the battle ends with no one gaining experience.

#### Determining turn order
Each turn, you determine turn order by rolling d20's and adding Speed modifiers. The highest goes first, unless an item or move states in its description that it overrides turn order (e.g. Quick Attack or Quick Claw).

#### Items
If you used an item, it will have its effect now, before attacks.

#### Attacks
In the order chosen earlier, carry out the attacks. If the attack text has "+n to hit", then you roll a d20 and add the specified modifier to it. If the attack is the same type as your Pokémon's primary type, roll two d20's and choose the highest (this is called STAB - Same Type Attack Bonus). Anything over 10 hits. On a hit, deal damage and any additional effect from the move's description.

##### Calculating damage
On a hit, attacks will say which die to roll for damage. When you deal damage using that attack, you work out the base damage by:
```
Dice roll + Attacker's Attack + Defenders Defence
```
If the attack is a Special attack, then you would use your Sp. Attack and their Sp. Defence instead of Attack and Defence.

If the enemy is of a type weak to the attack's type, double damage. If it is double weak (e.g. grass/psychic to bug), quadruple damage. Do the inverse for resistance (halve for resistant, quarter for double resistant, always rounded down with a minimum of 1). If it is immune to this damage type, reduce damage to 0. If you rolled a natural 20 to hit, then it is a critical hit and you can double the damage. This stacks, so if you critical hit on a double super effective attack you can deal 8x damage!

#### Fainting
When your or an opponent's Pokémon HP reaches 0, the Pokémon faints! It can no longer battle, and the opposing Pokémon gain experience.

#### Victory
When your opponent has no more non-fainted Pokémon, you win the battle!

# Levelling

#### Experience
When an enemy Pokémon faints, all Pokémon who fought that opponent gain experience according to the following sum:
```
enemy pokémon's level * 2 - your pokémon's level
```
...with a minimum exp of 1 (so you cannot gain 0 or negative exp).

#### Levelling up
When your Pokémon's experience points reach the same number as their level, that Pokémon levels up, resetting their experience to 0. Experience is applied one point at a time, so e.g. if a lvl2 Pokémon defeats a lvl4 Pokémon (for 4xp), it would gain 2 exp, level up to lvl3 (resetting exp to 0), then gain 2 more exp.

#### Why level up?
Levelling up will increase your Pokémon's base HP and enable more moves from their move set. Some Pokémon will also evolve at a certain level, improving their stats across the board.