## Requirements

-   [OBS Studio](https://obsproject.com/)
-   [OBS Python SDK for Websocket v5](https://github.com/aatikturk/obsws-python)

## About

A simple demonstration showing how to sync OBS scene switches to Voicemeeter states. The script assumes you have connection info saved in
a config file named `config.toml` placed next to `__main__.py`. It also assumes you have scenes named `START` `BRB` `END` and `LIVE`.

A valid `config.toml` file might look like this:

```toml
[connection]
host = "localhost"
port = 4455
password = "mystrongpass"
```

## Notes

For a similar Streamlabs Desktop example:

[Streamlabs example](https://github.com/onyx-and-iris/PySLOBS/blob/add-voicemeeter-example/examples/scenerotate.py)
