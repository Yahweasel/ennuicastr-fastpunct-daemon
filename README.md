This is an absurdly simple Unix domain socket server for
[fastPunct](https://github.com/notAI-tech/fastpunct). Connect to its socket,
and then give input like so:

```json
{"c":"fastpunct","i":["hello world"]}
```

It will respond like so:

```json
{"o":["Hello, world."]}
```

`ennuicastr-fastpunct-daemon.sh` is designed to install all dependencies in a
virtual environment automatically, so all you need to do to run the service is
run that.
