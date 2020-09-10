from sqlite3 import Error
import paho.mqtt.client as mqtt
import click
import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def insert_measurement_data(conn, data):
    try:
        c = conn.cursor()
        c.execute(f"INSERT INTO measurements (device, sensor, measurement, timestamp)"
                  f"VALUES ( '{data['device']}', '{data['sensor']}', {data['m']}, {data['t']} )")
        conn.commit()
    except Error as e:
        print(e)


def on_connect(client, userdata, flags, rc):
    print("[info]: Connected with result code "+str(rc))
    client.subscribe(userdata['topic'])


def on_message(client, userdata, msg):
    payload = yaml.load(msg.payload, Loader=yaml.FullLoader)
    try:
        insert_measurement_data(userdata['conn'], payload)
        if userdata.get('verbose', False):
            print(f"[info]: {msg.topic} {str(payload)}")
    except Exception as e:
        print(f'[error]: {e}')


@click.command()
@click.option('--broker',
              help='MQTT broker address')
@click.option('--port', default='1883',
              help='MQTT broker port')
@click.option('--db', default='sqlite',
              help="Database server to store data to (only supports sqlite3).")
@click.option('--dbfile', default='iotwx.db',
              help='Database file for sqlite3.')
@click.option('--verbose', is_flag=True,
              help="Will print output messages.")
@click.option('--topic', default='#',
              help="MQTT topic to subscribe to.")
def cli(broker, port, db, dbfile, topic, verbose):
    if db.strip() != 'sqlite':
        print(f"[exiting]: database {db} not supported.")
        exit()
    else:
        sql_create_measurement_table = \
            """
            CREATE TABLE IF NOT EXISTS
                measurements (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    device text NOT NULL,
                    sensor text NOT NULL,
                    measurement float NOT NULL,
                    timestamp long NOT NULL
                );
            """

        conn = create_connection(dbfile)

        if conn is not None:
            print(f"[info]: establishing connection to database {dbfile}")
            create_table(conn, sql_create_measurement_table)

            print(f"[info]: establishing connection to broker {broker} on topic {topic}")
            client = mqtt.Client(userdata={'conn': conn, 'topic': topic, 'verbose': verbose})
            client.on_connect = on_connect
            client.on_message = on_message
            client.connect(broker, int(port), 60)
            client.loop_forever()
        else:
            print("[error]: Could not establish a connection to broker.  Exiting.")
            exit()