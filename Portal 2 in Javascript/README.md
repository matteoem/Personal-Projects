# PORTAL 2
![Alt text](https://upload.wikimedia.org/wikipedia/it/d/df/Portal_logo.png)

RECREATION OF THE GAME PORTAL.

PORTAL 2 is a Puzzle game-like published by Valve Corporation in 2011. This recreation in javascript using three.js & physi.js wants to be the sincerest form of flattery for
the beatiful masterpiece of videogame that Portal is.
- The link for trying the game is on the bottom of this file.
- if you want to give me any feedback as a user, feel free to contact me!

![Alt text](https://i.gyazo.com/05ff2d83af11e9547510557b34650990.png)


The commands are stated also in the starting Menu,but here will be reported again:

- ![#0000ff](https://via.placeholder.com/15/ff0000/000000?text=+) `lock your mouse pressing CTRL. You can esc from this mouse pointer-less mode pressing ESC`
- ![#0000ff](https://via.placeholder.com/15/c8c8c8/000000?text=+) `Use W-A-S-D to move around`
- ![#0000ff](https://via.placeholder.com/15/c8c8c8/000000?text=+) `Hold shift to sprint`
- ![#0000ff](https://via.placeholder.com/15/c8c8c8/000000?text=+) `Grab The Companion Cubes with E`
- ![#0000ff](https://via.placeholder.com/15/c8c8c8/000000?text=+) `Jump with SPACE`
- ![#0000ff](https://via.placeholder.com/15/0000ff/000000?text=+) `Use the LEFT MOUSE BUTTON to shoot the BLUE portal`
- ![#ffa500](https://via.placeholder.com/15/ffa500/000000?text=+) `Use the RIGHT MOUSE BUTTON to shoot the ORANGE portal`
- ![#0000ff](https://via.placeholder.com/15/c8c8c8/000000?text=+) `Use R to turn on/off the light`



# Important statement:
The mechanics that I tried to implement are extremely complex, unoptimized(for as it is now..) and very powerful. 
This brings along the major problem that if you force such mechanics,you will be able to break it. For that I implemented some respawn conditions to help the experience. 

***Known Bugs*** :
- I'm aware of how the force imprinted to the companion cubes passing the portals is slightly unstable. Don't worry, the cubes will respawn in the same spot where you found it
if they will break through the wall of the map.
- if you try to enter inside the portals with specific combination of linear velocities-directions, you may not be able to pass by. It happens very,very rarely,but still happen.
- With some browsers version, ***you may have some things that are not loaded properly***, or even crashes before the start of the game,remaining stucked in the loading screen. In this case, I suggest to try with another browser.
- if you are having trouble with the ***mouse being locked*** remember the command to enter and exit the locked mouse mode. If they are not working, it's because of some issue related to the browser itself
- In some users the portalgun sound that occure when pressing L/R mouse button, use to be missing. It's an issue related to the loading of the browser. It will not break anything,exept the fact that the gun will not emit any sound when shooting
- the game requires to render 3 cameras when the portals are up. This makes the game heavy, so ***be aware*** that without a computer with average performance requirement you may experience lag.
- The video played in loop in the plasma TV, use to not render from time to time. 
- the cubes happen to get stucked outside of the physic engine when trying to pass through a portal while having the cube grabbed.
- Firefox experience more lag than other browsers. Chrome, Opera and Edge are recommended.
- For few users, even with the optimal machine to run the game, heavy lag was experienced. This happened to be a very isolated event found only by two users. I'm investigating the reason behind this, but it is a hard bug to deal with given the fact that I cannot replicate such error with the machine I have.

***Fixed bugs*** :
- fixed the camera adjustment when coming out of a portal placed upside down,or with strange angles with respect to the other portal.
- added the possibility to fell forever between two portal in vertical line(signature feature for portal!)
- added the hidden control that does not allow the portals to spawn with partially compenetrated outline on other object. From now on,if you try to create a portal on a surface where there is not enough space for it to appear, the gun will just not fire.
- ***partially*** fixed the problem of the companion cube flying away when passing through the portal. This is probably the hardest fix to do, having to deal with the forces. Some major improvement has been done so far though.
- fixed the problem of the signature radio from Portal that used to disappear,giving trouble with the loader.

***Upcoming improvements***:
- Change the system with which the pressure button activate, swapping from a raycast system to a collision callback-based system.

Thanks for trying this game,and remember...

![Alt text](https://i.gyazo.com/8526fde911ebaa483f37ea63eb699a82.png)

# the cake is a lie,but the fun is not. So have fun!

*You can try the game here!* [PORTAL 2](https://sapienzainteractivegraphicscourse.github.io/final-project-matteoem/) 


Made By Matteo Emanuele

P.S. if you want to download this project or make any use, please ask first to matteoemanuele0@gmail.com
