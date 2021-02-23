# About

This is a program that lets you customise OptiFine capes. 
The program first loads capes from your local `capes` folder. If no cape is found, it checks for one in this github repository. If still no cape is found, it will check for an official optifine cape. Finally, if no OptiFine cape is found, it loads a default cape file (Currently the migration cape). 

To use a custom cape, create a `capes` folder next to the program file, and paste in your custom cape. The cape must also contain an Elytra texture. Make sure the cape file is named after your Minecraft username.

**DISCLAIMER**, these changes are purely client side, and no one else can see them.
If you want your cape added to this github repository, so that other people using this program can see it, then join my [Discord Server](https://discord.com/invite/pkRxtGw) and send your cape and username in the `#custom-capes` channel.

# Setup

Start by downloading the program from [here](https://github.com/ewanhowell5195/customOptiFineCapeServer/releases/tag/customOptiFineCapeServer1.2)

To use this, you need to edit your `hosts` file. 

Start by opening `Notepad.exe` in Administrator mode. You can do this by searching it in the windows seach bar, right clicking it, and selecting `Run as Administrator`

From Notepad, go to `File->Open` and open the file `C:/Windows/System32/drivers/etc/hosts`
If you cannot see the file, make sure that `All Files (*.*)` is selected in the bottom right corner.

Next, add `127.0.0.1 s.optifine.net` to the bottom of the file, and save the file.

Finally, run `ipconfig /flushdns` in command prompt and then you are done!

Just launch the downloaded program to begin. If it looks like nothing happens when you run it, you can check in task manager to see if it is running in the background.

# Custom Default Capes

If a player does not have a cape set, they will have a default cape applied.
In the `settings.json`, you can define a custom directory to load default capes from.
If there are multiple textures in the default cape directory, players will be given a random one.
Full instructions in the `settings.json` file.

# Resource Pack Support

If the custom default directory is set to `resource-pack`, it will load the default capes from `assets/minecraft/textures/capes` of the current top loaded resource-pack.
If no capes are found in a resource pack, it will load them from a folder called `default` located next to the program file.

# Auto starting

If you want to make this program start with Windows and run in the background, so you don't have to launch it every time you play Minecraft, start by copying the downloaded program file.
Next navigate to the folder `C:/Users/<user>/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Start-up` , right click, and select `Paste shortcut`.

# Remove Notifications

If you want to disable the notifications that show whenever you start the program, open the `settings.json` file and change `notifications` from `true` to `false`.
If you do not have a `settings.json` file, run the program once and it will appear.

# Uninstallation

To uninstall this, you need to open your `hosts` file again and remove `127.0.0.1 s.optifine.net`

# Confirmed Working Versions

- Optifine
- Forge + OptiFine