# Twiddler Configuration File Parser

Usage:

```
    from twiddler_config import Config

    cfg = Config.from_path('/path/to/my/twiddler.cfg')

    print(cfg.version)
    print(cfg.chords)
    # etc
```

## Command-line Utility

The included command-line utility provides a variety of tools organized
by subcommand described below.

### `chords`: Display all chords in a configuration

You can print a brief description of your Twiddler configuration, including
all of its included chords by running:

```
    twiddler-config chords /path/to/my/twiddler.cfg
```

### `table`: Display chord tables

You can print a chord tables in the style of Backspice2
by running:

```
    twiddler-config table /path/to/my/twiddler.cfg
```

Optional arguments:

* `--right-to-left`: Instead of printing chords in three columns
  from left to right, print the columns in right-to-left order.
