# ESPHome LG AC Wired Controller (External Component)

ESPHome external component for controlling LG air conditioners over the wired CN-REMO connection.

For the original project — including hardware setup, PCB designs, wiring, and protocol details — see <https://github.com/JanM321/esphome-lg-controller>.

## Usage

Add the component source to your device YAML:

```yaml
external_components:
  - source: github://GraphicHealer/esphome-lg-controller@main
    components: [lg_controller]
```

Then configure the `climate` platform, a `uart:` connection, and the usual ESPHome boilerplate (`esp32:`, `api:`, `wifi:`, `ota:`, `logger:`).

## Example Configuration

```yaml
substitutions:
  deviceid: 'lglivingroom'
  devicename: 'LG Living Room'
  temperature_sensor_entity_id: sensor.my_sensor

esphome:
  name: ${deviceid}
  friendly_name: ${devicename}

esp32:
  board: esp32dev
  framework:
    type: esp-idf

uart:
  - id: ac_serial
    tx_pin: GPIO25
    rx_pin:
      number: GPIO26
      allow_other_uses: true
    baud_rate: 104

external_components:
  - source: github://GraphicHealer/esphome-lg-controller@main
    components: [lg_controller]
    refresh: 0s

time:
  - platform: homeassistant
    id: homeassistant_time

sensor:
  - id: temp_sensor
    platform: homeassistant
    internal: true
    entity_id: ${temperature_sensor_entity_id}
  - platform: uptime
    type: timestamp
    name: 'Last Boot'

api:
  encryption:
    key: 'my_key'

wifi:
  ssid: 'wifi-SSID'
  password: 'wifi-password'

  ap:
    ssid: '${deviceid} Fallback Hotspot'
    password: 'hotspot-password'

captive_portal:

ota:
  platform: esphome

logger:
  level: DEBUG

climate:
  - platform: lg_controller
    name: ''
    id: ${deviceid}
    uart_id: ac_serial
    rx_pin:
      number: GPIO26
      allow_other_uses: true
    fahrenheit: false
    is_slave_controller: false
    temperature_sensor: temp_sensor
    vane1:
      name: 'Airflow 1 Up-Down'
      id: vane_position_1
      icon: mdi:arrow-up-down
    vane2:
      name: 'Airflow 2 Up-Down'
      id: vane_position_2
      icon: mdi:arrow-up-down
    vane3:
      name: 'Airflow 3 Up-Down'
      id: vane_position_3
      icon: mdi:arrow-up-down
    vane4:
      name: 'Airflow 4 Up-Down'
      id: vane_position_4
      icon: mdi:arrow-up-down
    overheating:
      name: 'Over Heating'
      id: overheating
      icon: mdi:heating-coil
    fan_speed_slow:
      name: 'Fan Speed Slow'
      id: fan_speed_slow
      icon: mdi:fan-chevron-down
      mode: box
    fan_speed_low:
      name: 'Fan Speed Low'
      id: fan_speed_low
      icon: mdi:fan-speed-1
      mode: box
    fan_speed_medium:
      name: 'Fan Speed Medium'
      id: fan_speed_medium
      icon: mdi:fan-speed-2
      mode: box
    fan_speed_high:
      name: 'Fan Speed High'
      id: fan_speed_high
      icon: mdi:fan-speed-3
      mode: box
    sleep_timer:
      name: 'Sleep Timer (minutes)'
      id: sleep_timer
      icon: mdi:timer-outline
      mode: box
    error_code:
      name: 'Error Code'
      id: error_code
      icon: mdi:alert-circle-outline
    pipe_temp_in:
      name: 'Pipe Temperature In'
      id: pipe_temperature_in
      icon: mdi:thermometer
      unit_of_measurement: '°C'
    pipe_temp_mid:
      name: 'Pipe Temperature Mid'
      id: pipe_temperature_mid
      icon: mdi:thermometer
      unit_of_measurement: '°C'
    pipe_temp_out:
      name: 'Pipe Temperature Out'
      id: pipe_temperature_out
      icon: mdi:thermometer
      unit_of_measurement: '°C'
    defrost:
      name: 'Defrost'
      id: defrost
      icon: mdi:snowflake-melt
    preheat:
      name: 'Preheat'
      id: preheat
      icon: mdi:heat-wave
    outdoor:
      name: 'Outdoor Unit'
      id: outdoor
      icon: mdi:fan
    auto_dry_active:
      name: 'Auto Dry Active'
      id: auto_dry_active
      icon: mdi:fan-clock
    purifier:
      name: 'Air Purifier'
      id: air_purifier
      icon: mdi:pine-tree
    internal_thermistor:
      name: 'Internal Thermistor'
      id: internal_thermistor
      icon: mdi:thermometer
    auto_dry:
      name: 'Auto Dry'
      id: auto_dry
      icon: mdi:fan-clock
```

### Substitutions used above

- `${deviceid}`: Unique ESPHome device ID.
- `${devicename}`: Friendly name shown in Home Assistant.
- `${temperature_sensor_entity_id}`: Entity ID of the Home Assistant temperature sensor used as the room temperature.

## Configuration Options

### `climate` platform

- `uart_id` (**required**): The `id` of the `uart:` component connected to the AC.
- `rx_pin` (**required**): GPIO receiving the AC serial signal. Must match the `rx_pin` configured in `uart:`.
- `fahrenheit` (**required**, `true`/`false`): Use Fahrenheit setpoints and displays.
- `is_slave_controller` (**required**, `true`/`false`): Set to `true` if a second controller is the master on the same indoor unit.
- `temperature_sensor` (*optional*): `id` of a sensor providing the room temperature. If omitted, the AC's internal thermistor is used.
- `vane1` – `vane4` (**required**): `select:` entities for up/down airflow positions. Options are `0 (Default)` through `6 (Down)`.
- `overheating` (**required**): `select:` entity with installer over-heating settings. Options are `0 (Default)`, `1 (+4C/+6C)`, `2 (+2C/+4C)`, `3 (-1C/+1C)`, `4 (-0.5C/+0.5C)`.
- `fan_speed_slow`, `fan_speed_low`, `fan_speed_medium`, `fan_speed_high` (**required**): `number:` entities (0–255) for the installer fan speed settings.
- `sleep_timer` (**required**): `number:` entity (0–420 minutes).
- `error_code`, `pipe_temp_in`, `pipe_temp_mid`, `pipe_temp_out` (**required**): `sensor:` entities reporting diagnostics.
- `defrost`, `preheat`, `outdoor`, `auto_dry_active` (**required**): `binary_sensor:` entities reporting status flags.
- `purifier`, `internal_thermistor`, `auto_dry` (**required**): `switch:` entities.

### Notes

- The `tx_pin` in `uart:` is unused by the component but must be defined for the ESPHome `uart` platform. You can set it to an unused GPIO.
- The `rx_pin` must be passed both in `uart: rx_pin:` and in the `climate:` `rx_pin:` so the component can control the pin directly.
- The `uart:` `baud_rate` is always **104** for the LG wired controller.

## License

This project is licensed under the 0BSD License. See the LICENSE file for details.
