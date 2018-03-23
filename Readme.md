# Fidget Spinner Game - Cool Fidget Spinner Game for Sam's Science Fair
Kids love this one, who can spin the longest?  Who can spin the fastest? Find out using this project!

![Finished](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/finished.jpg "Finished")
![Finished](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/finished2.jpg "Finished")

#### Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
> 
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
> 
> $ `umount /dev/sdb1`
> 
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
> 
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
> 
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
>
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "FidgetSpinner"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update`
>
>$ `sudo apt-get upgrade`
>
>$ `sudo apt-get install vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-gpiozero python-psutil`

**Update local timezone settings

>$ `sudo dpkg-reconfigure tzdata`

`select your timezone using the interface`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>
>`alias l='ls -lh'`
>
>`source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>`sudo vi  /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

**Clone Game repository**

>$ `cd ~`
>
>$ `git clone https://github.com/khinds10/FidgetSpinnerGame.git`

**Install i2c Backpack Python Drivers**

>$ `cd ~`
>
>$ `git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack`
>
>$ `cd Adafruit_Python_LED_Backpack/`
>
>$ `sudo python setup.py install`
>

### Setup the scripts to run at boot
`crontab -e`

Add the following lines 

`@reboot /bin/sleep 15; nohup python /home/pi/FidgetSpinnerGame/player1.py > /home/pi/FidgetSpinnerGame/player1.log 2>&1`
`@reboot /bin/sleep 15; nohup python /home/pi/FidgetSpinnerGame/player2.py > /home/pi/FidgetSpinnerGame/player1.log 2>&1`

### Supplies Needed

For the below supplies list I went with yellow vs green for team colors, however you can pick, red vs blue etc.

**Small thin sheet of plywood**

![Plywood](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/plywood.png "Plywood")

**RaspberriPi Zero**

![Pi Zero](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/pi-zero.png "Pi Zero")

**LED Illuminated Push button Built-in Switch 5V Button (yellow / green)**

![Yellow LED Illuminated Button](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/yellow-button.png "Yellow LED Illuminated Button")

![Green LED Illuminated Button](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/green-button.png "Green LED Illuminated Button")

**7-segment Display W/i2c Backpack (yellow)**

![Yellow Display](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/yellow.jpg "Yellow Display")

**7-segment Display W/i2c Backpack (green)**

![Green Display](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/green.png "Green Display")

## Preparing Hardware

Solder Unique Display Jumpers
*NOTE: All the I2C backpacks must be soldered on the back of each of the displays, the backpacks come with the display and must all be soldered on first.*

For each of the I2C backpack displays you must solder the jumpers on the back in the **4 different possible combinations** to have your RaspberriPI I2C interface to recognize each display with a **unique address**.  

Leave the first display with no jumper soldered, the 2nd with the farthest right soldered, the 3rd with only the middle soldered and so on...  

*There's a total of 3 pins so you should have a total combination of 8 unique combinations.*

![Solder Unique Display Jumpers](https://raw.githubusercontent.com/khinds10/RetroDashboard/master/construction/displays.jpg "Solder Unique Display Jumpers")

### Wiring Diagram

![Wiring Diagram](https://raw.githubusercontent.com/khinds10/RetroDashboard/master/construction/wiring-diagram.png "Wiring Diagram")

### Test 7 Segment Display I2C Connectivity

Start up your RaspberryPi and make sure the I2C bus recognizes all your connected 7 segment displays. 
*[each display is given a unique address described above by how you solder each display's jumpers in different combinations]*

If you have all 4 displays with jumpers soldered in all 4 combinations, you should have the following output for the `i2cdetect` command:

`sudo i2cdetect -y 1`
     
>    0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
>
> 00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
> 
> 70: 70 71 72 73 -- -- -- --

*(in this case all the displays numbered 0 to 4 are being recognized on the PI as I2C available devices)*

### Building the Game

Using a 3d printer and the provided (.stl) files in the /enclosure folder of this project print the button and display cases and the 6 small squares used to attach to the bottom of the plywood to hold the game board slightly off the table for wiring.

Paint the board to mount the button, RaspberriPi and 7 Seg. Displays

![Paint Board](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/paint.jpg "Paint Board")

Connect the Displays and buttons accordingly with wired leads

![Wire Displays & Buttons](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/wire-displays.jpg "Wire Displays & Buttons")

Gather Parts to assemble on the board, drill holes where the wires will be feed through below to connect everything

![Gather Parts](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/gather-parts.jpg "Gather Parts")


Wire the Board from below, feeding the wires through the drilled holes in the board

![Wire the Board](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/wire-board.jpg "Wire the Board")

Mount/Connect the RaspberriPi to the correct leads

![Connect RPi](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/connect-pi.jpg "Connect RPi")

### Finished!

![Finished](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/finished.jpg "Finished")
![Finished](https://raw.githubusercontent.com/khinds10/FidgetSpinnerGame/master/construction/finished2.jpg "Finished")
