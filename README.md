# Purpose

Store data from IoTwx MQTT messages into a sqlite3 database.

# Installation

```bash
$ pip install --editable .
```

# Usage

```bash
$ iotwx2db --help
```

```
Usage: iotwx2db [OPTIONS]

Options:
  --broker TEXT  MQTT broker address
  --port TEXT    MQTT broker port
  --db TEXT      Database server to store data to (only supports sqlite3).
  --dbfile TEXT  Database file for sqlite3.
  --verbose      Will print output messages.
  --topic TEXT   MQTT topic to subscribe to.
  --help         Show this message and exit.
```

# Example
```
$ iotwx2db --broker your.broker.com --topics the/topics/to/capture
```

# Schema

```sql
measurements (
   id integer PRIMARY KEY AUTOINCREMENT,
   device text NOT NULL,
   sensor text NOT NULL,
   measurement float NOT NULL,
   timestamp long NOT NULL
)
```



Have fun!
