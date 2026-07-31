import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate, sensor, uart
from esphome.const import CONF_ID

CODEOWNERS = ["JanM321"]
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]

lg_pqrcuds0_ns = cg.esphome_ns.namespace("lg_pqrcuds0")
LgHvac = lg_pqrcuds0_ns.class_(
    "LgHvac", cg.PollingComponent, uart.UARTDevice, climate.Climate
)

CONF_REFERENCE_TEMPERATURE = "reference_temperature"

CONFIG_SCHEMA = climate.climate_schema(LgHvac).extend(
    {
        cv.Required(CONF_REFERENCE_TEMPERATURE): cv.use_id(sensor.Sensor),
    }
).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    await uart.register_uart_device(var, config)

    temp = await cg.get_variable(config[CONF_REFERENCE_TEMPERATURE])
    cg.add(var.set_reference_temperature(temp))
