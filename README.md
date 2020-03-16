# AKAI-LPD8
My friend told me to code it, not sure why tho

## What?

My friend gave me AKAI LPD8 and told me to read the MIDI stream and prepare it to be sent via MQTT and wrap it all into some python package. I've never used MQTT before. Nor the packages. And I'm low on caffeine.

## What about the lights

I have some RGB controller made by BleBox and I would like to control it via AKAI.
Three knobs should control red, green, and blue diodes. Tapping pads for the "boom" effect or setting a blinking tempo would be a nice feaure.

## Issues

### Known

1. Knob 8 has some physical glitches. When turned clock-wise to the end of range after the value exceeds 127 it comes back to 90-some to reach again 127.

2. My current knowledge indicates that there is no way to get a current state of a knob.

### Resolved

1. I've used Mido as a MIDI library. It requires `rtmidi`. To install it properly instead of installing it via `pip` I had to run
`apt install python3-rtmidi`.
