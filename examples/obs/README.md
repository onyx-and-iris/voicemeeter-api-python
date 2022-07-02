## Requirements

-   [OBS Studio](https://obsproject.com/)
-   [OBS Websocket Plugin](https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-from-websockets.466/)
-   [OBS Websocket Py](https://github.com/onyx-and-iris/obs-websocket-py)

## About

A simple demonstration showing how to sync OBS scene switches to Voicemeeter states. The script assumes you have connection info saved in
a config file named `config.ini` placed next to `__main__.py`. It also assumes you have scenes named `START` `BRB` `END` and `LIVE`.

A valid `config.ini` file might look like this:

```ini
[connection]
ip=localhost
port=4444
password=mystrongpassword
```
