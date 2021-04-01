# Nanome - Structure Prep

A Nanome Plugin to add bonds and secondary structures to complexes. Useful for Nanome Quest, as those features are not available natively.

## Dependencies

[Docker](https://docs.docker.com/get-docker/)

## Usage

To run Structure Prep in a Docker container:

```sh
$ cd docker
$ ./build.sh
$ ./deploy.sh -a <plugin_server_address> [optional args]
```

## Development

To run Structure Prep with autoreload:

```sh
$ python3 -m pip install -r requirements.txt
$ python3 run.py -r -a <plugin_server_address> [optional args]
```

## License

MIT
