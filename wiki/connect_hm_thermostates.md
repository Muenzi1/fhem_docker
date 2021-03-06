# Effective use of HM-CC-RT-DN with FHEM

## How to use HM-MOD-RPI-PCB to connect HM-CC-RT-DN with FHEM

### Enable UART on RPI3+

1. Deactivate the exclusive use of the console for ttyAMA0

    ```bash
    systemctl stop serial-getty@ttyAMA0.service
    systemctl disable serial-getty@ttyAMA0.service
    systemctl mask serial-getty@ttyAMA0.service
    ```

2. Enable and configure UART in /boot/config.txt by appending this

    ```bash
    enable_uart=1
    dtoverlay=miniuart-bt
    core_freq=250
    ```

3. Restart the Raspberry PI

    ```bash
    sudo reboot
    ```

### Add UART port to FHEM container

Just add ttyAMA0 as DEVICE to docker-compose.yml in the fhem container section

```bash
devices:
    - "/dev/ttyAMA0:/dev/ttyAMA0"
```

and recreate the container.

### Add HM-MOD-RPI-PCB module to FHEM

1. Very important, disable automatic check for USB devices as they can overload FHEM. To disable this, run this line in FHEM.

    ```bash
    attr initialUsbCheck disable 1
    ```

2. Define HMUARTLGW device

    ```bash
    define myHmUART HMUARTLGW /dev/ttyAMA0
    ```

3. OPTIONAL: Define VCCU - honestly, I think this is not necessary, but in my tests the pairing went wrong as long as
   this device was not defined

    ```bash
    define VCCU CUL_HM AABBCC
    attr VCCU IODev myHmUART
    ```

    AABBCC is basically just a random HM-ID.

4. Enter pairing mode for 120 seconds

    ```bash
    set myHmUART hmPairForSec 120s
    ```

5. Enter pairing mode at the HM-CC-RT-DN. Be warned, you might need to reset the thermostate first.
6. The device will show up with its HM-ID in FHEM. But most likely it will not fully paired after the first try. If it
   is not fully paired, enter pairing mode a few times more and use burstXmit until it worked. Probably you also need to
   use the FHEM delete mode a few times after each pairing try.

7. If it finally connected well, rename the device

    ```bash
    set OLD_DEVICE_NAME deviceRename NEW_DEVICE_NAME
    ```

8. Avoid logging HM data twice for the HM and the HM_Clima device.

    ```bash
    attr NEW_DEVICE_NAME_Clima DbLogExclude desired-temp,ValvePosition
    ```

Sources of this wrapup:
<https://wiki.fhem.de/wiki/Raspberry_Pi#Verwendung_UART_f.C3.BCr_Zusatzmodule>  
<https://wiki.fhem.de/wiki/HMUARTLGW>  
<https://techblog.one/homematic-mit-der-cul-guenstig-unter-fhem-einbinden/>  

## Use external ESPEasy as temperature sensor for HM-CC-RT-DN

1. Create hminfo device

    ```bash
    define hm HMinfo
    ```

2. Define virtual HM device

    ```bash
    define vt_bz_heizung CUL_HM AAABB1
    set vt_bz_heizung virtual 1
    rename vt_bz_heizung_Btn1 bz_heizung_Sensor1
    set bz_heizung_Sensor1 peerChan 0 bz_heizung_Weather single set
    ```

    with HM-ID need to be a unique identifier.

3. Update temperature in HM device on new ESPEasy measurements

    ```bash
    define at_bz_vt notify ESPEasy_Badezimmer_BMP:Temperature:.* set bz_heizung_Sensor1 virtTemp $EVTPART1
    ```
