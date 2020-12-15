# met.no precipitation now cast component

This component will add a sensor for met.no precipitation now cast. The sensor shows the maximum amount of precipitation for the next 90 minutes. Detailed precipitation data is available in the 'forecast' attribute.

https://api.met.no/weatherapi/nowcast/2.0/documentation


## HACS Installation

1. Open HACS Settings
2. Add `https://github.com/toringer/home-assistant-metnowcast` as a custom repository 
2. Add the code to your `configuration.yaml` using the config options below.
3. **You will need to restart after installation for the component to start working.**



## Sample Sensor Configuration

    sensor:
    - platform: metnowcast