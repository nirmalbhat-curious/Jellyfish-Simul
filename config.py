# ==========================================
# JELLYFISH SIMULATOR - ENVIRONMENT SETTINGS
# ==========================================


class EnvironmentConfig:

    # --------------------------------------
    # OCEAN CONDITIONS
    # --------------------------------------

    TEMPERATURE = 20.0       # Temperature in Celsius
    PH = 8.1                 # Ocean pH

    # --------------------------------------
    # OCEAN CURRENT SETTINGS
    # --------------------------------------

    CURRENT_STRENGTH = 0.35
    CURRENT_VARIABILITY = 0.15

    CURRENT_CHANGE_SPEED = 0.5

    # --------------------------------------
    # WAVE SETTINGS
    # --------------------------------------

    WAVE_SPEED = 1.5
    WAVE_AMPLITUDE = 12
    WAVE_FREQUENCY = 0.05

    # --------------------------------------
    # POLLUTION SETTINGS
    # --------------------------------------

    POLLUTION_INTENSITY = 1.0

    POLLUTION_STRESS_FACTOR = 0.5

    # --------------------------------------
    # JELLYFISH SETTINGS
    # --------------------------------------

    NORMAL_SWIMMING_SPEED = 2.0

    MIN_SWIMMING_SPEED = 0.5
    MAX_SWIMMING_SPEED = 3.0

    NORMAL_STRESS = 0.0

    # --------------------------------------
    # ENVIRONMENTAL LIMITS
    # --------------------------------------

    MIN_TEMPERATURE = 0.0
    MAX_TEMPERATURE = 35.0

    MIN_PH = 6.0
    MAX_PH = 9.0