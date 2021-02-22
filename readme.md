# About

This is a program that lets you customise OptiFine capes. 
The program first loads capes from your local `capes` folder. If no cape is found, it checks for one in this github repository. If still no cape is found, it will check for an official optifine cape. Finally, if no OptiFine cape is found, it loads a default cape file (Currently the migration cape). 

To create a custom cape, create a `capes` folder next to the program file, and paste in your custom cape. The cape must also contain an Elytra texture. Make sure the cape file is named after your Minecraft username.

**DISCLAIMER**, these changes are purely client side, and no one else can see them.
If you want your cape added to this github repository, so that other people using this program can see it, then join my [Discord Server](https://discord.com/invite/pkRxtGw) and send your cape and username in the `#custom-capes` channel.

# Setup

Start by downloading the program from [here](https://github.com/ewanhowell5195/customOptiFineCapeServer/releases/tag/customOptiFineCapeServer)

To use this, you need to edit your `hosts` file. 

Start by opening `Notepad.exe` in Administrator mode. You can do this by searching it in the windows seach bar, right clicking it, and selecting `Run as Administrator`

From Notepad, go to `File->Open` and open the file `C:\Windows\System32\drivers\etc\hosts`
If you cannot see the file, make sure that `All Files (*.*)` is selected in the bottom right corner.

Next, add `127.0.0.1 s.optifine.net` to the bottom of the file, and save the file.

# Auto starting

If you want to make this program start with Windows and run in the background, so you don't have to launch it every time you play Minecraft, start by copying the downloaded program file.
Next navigate to the folder `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` , right click, and select `Paste shortcut`.

# Remove Notifications

If you want to disable the notifications that show whenever you start the program, in the shortcut you just made to the file, right click it and go to `Properties`. 
In the `Target` text field, add a space after the file path and add `-silent`

# Uninstallation

To uninstall this, you need to open your `hosts` file again and remove `127.0.0.1 s.optifine.net`

# Tested Clients

### Working
- Vanilla Minecraft with OptiFine
-  
