# Wireless Pico PC Sensor Monitor

![Pico PC Sensor Monitor UI](https://cdn-images-1.medium.com/max/800/1*Ts2UdS8WdyrMtb4bxQJMbg.gif)

Wireless Pico PC Sensor Monitor with power consumption calculator using Raspberry Pi Pico W. It does not require a wired connection to your PC. For the more detailed guide you can visit article on Medium.


## Hardware requirements
- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/?variant=raspberry-pi-pico-w)
- [1.14 inch LCD screen panel](https://www.waveshare.com/pico-lcd-1.14.htm) or any other compatible panel with ST7789 and 240x135 resolution

## Prerequisites
1. Install [Open Hardware Monitor](https://openhardwaremonitor.org/);
2. Enable Open Hardware Monitor internal web server, enable it to start minimized at tray on Windows startup;
3. Bind the current or desired IP for your PC in your router;
4. Enable port in your Windows firewall (8085 by default);

## Setup Raspberry Pi Pico W
1. Connect Pi Pico to your PC and Install [Micropython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython);
2. Clone this project to the local directory;
3. Edit the following lines in config.py to get it started:

![Pico PC Sensor Monitor UI](https://cdn-images-1.medium.com/max/800/1*rDi2Yaci8IelU5m_WsLkMg.png)

- line 2: change the IP:Port string to the one you have at step [2] of Prerequisites;
- lines 6,8: your Wi-Fi credentials;
- line 11: your local electricity cost per kWh in any currency;
- there are some more parameters to finetune from this file.

4. Copy all the files to Pi Pico using [Rshell](https://github.com/dhylands/rshell), ThonyIDE, etc.
5. Restart Pi Pico


## Pico PC Sensor Monitor UI

![Pico PC Sensor Monitor UI](https://cdn-images-1.medium.com/max/800/1*qGJym1IlQOn8vvtdfmZXfA.png)

- The green text shows the installed devices wattage on the left, current temperatures on the right. The color will change when the values are increasing from green to red;
-The large magenta text at the bottom half of the screen is the current  total wattage;
-The framed small magenta text in the middle right: 
 - $$/h: the cost of energy per hour with the current system load;
 - Total $: the accumulated cost for the electricity spent for the current session;
- (Optionally) It is possible to change brightness of the screen with A and B hardware buttons if you have the ones.
