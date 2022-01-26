from .check_rpi import check_rpi

if check_rpi():
    from .i2c import I2C as I2C
    from .pin import Pin as Pin
else:
    # TODO: logger?
    print("Not running on RPI! Importing dummy drivers.")
    from .i2c_dummy import I2C as I2C
    from .pin_dummy import Pin as Pin
