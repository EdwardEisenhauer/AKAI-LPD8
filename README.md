# AKAI-LPD8

My friend gave me an AKAI LPD8 MIDI interface and asked me to prepare a library to precess MIDI stream into something that could be sent via MQTT. I've never used MQTT before.

## Structure

### Sideproject - akai-to-wLightBox.py

I have a Blebox wLightBox RGB to control the LED strip in my room. We thought it would be nice to use its API to control it via AKAI.

Currently, the following features are included:

Knobs:
  - R, G, B, and W intensity
  - colour and effect fading, and effect step durations (from 0 to 1000ms)
  - effect mode (one out of 7 predefined by BleBox)

Pads:
  - R, G, B, and W toggling

#### Usage

Just run ```python3 akai-to-wLightBox.py IP``` providing it with wLightBox's IP address.

### wLightBox.py

Used to communicate with the wLightBox via its API (simple GET and POST requests with JSON).

### akai.py

Used to listen for the incoming MIDI messages.

## TODO
  - [ ] introduce an MQTT module
  - [ ] do something with the shared viariables in akai.py
  - [ ] rewrite interepolate functions to convert knob positions into bpms

## Known issues

1. Knob 8 has some physical glitches. When turned clockwise to the end of range after the value exceeds 127 it comes back to 90-some to reach again 127.
  1. All the knobs are sometimes glitchy.

2. My current knowledge indicates that there is no way to get a current state of a knob (due to the MIDI architecture).

### Resolved (may be helpful for the visitors)

1. I've used Mido as a MIDI library. It requires `rtmidi`. To install it properly instead of installing it via `pip` I had to run
`apt install python3-rtmidi`.
