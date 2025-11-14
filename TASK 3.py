import logging

# ---------------------------------
# Logging Configuration
# ---------------------------------
logging.basicConfig(
    filename="temperature_converter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------
# Temperature Converter Class
# ---------------------------------
class TemperatureConverter:
    @staticmethod
    def c_to_f(c):
        return (c * 9/5) + 32

    @staticmethod
    def f_to_c(f):
        return (f - 32) * 5/9

    @staticmethod
    def c_to_k(c):
        return c + 273.15

    @staticmethod
    def k_to_c(k):
        return k - 273.15

    @staticmethod
    def f_to_k(f):
        return (f - 32) * 5/9 + 273.15

    @staticmethod
    def k_to_f(k):
        return (k - 273.15) * 9/5 + 32


# ---------------------------------
# Utility Functions
# ---------------------------------
def get_float_input(prompt):
    """Safely get a valid float input from user"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("⚠ Invalid input! Please enter a numeric value.")


def choose_unit(prompt):
    """Choose temperature unit"""
    units = {"1": "C", "2": "F", "3": "K"}
    print(prompt)
    print("1. Celsius (C)")
    print("2. Fahrenheit (F)")
    print("3. Kelvin (K)")

    while True:
        choice = input("Select an option (1/2/3): ").strip()
        if choice in units:
            return units[choice]
        print("⚠ Please enter a valid choice (1, 2, or 3).")


# ---------------------------------
# Main Conversion Logic
# ---------------------------------
def convert_temperature(value, from_unit, to_unit):
    conv = TemperatureConverter()

    if from_unit == "C" and to_unit == "F":
        return conv.c_to_f(value)
    elif from_unit == "F" and to_unit == "C":
        return conv.f_to_c(value)
    elif from_unit == "C" and to_unit == "K":
        return conv.c_to_k(value)
    elif from_unit == "K" and to_unit == "C":
        return conv.k_to_c(value)
    elif from_unit == "F" and to_unit == "K":
        return conv.f_to_k(value)
    elif from_unit == "K" and to_unit == "F":
        return conv.k_to_f(value)
    else:
        return value  # same unit conversion


# ---------------------------------
# Program Entry Point
# ---------------------------------
def main():
    print("\n🌡️  Advanced Temperature Converter")
    print("====================================\n")

    temp_value = get_float_input("Enter the temperature value: ")

    from_unit = choose_unit("\nConvert From:")
    to_unit = choose_unit("\nConvert To:")

    result = convert_temperature(temp_value, from_unit, to_unit)

    print(f"\n✅ Converted Temperature: {temp_value}°{from_unit} → {result:.2f}°{to_unit}")

    logging.info(
        "Converted %.2f %s to %.2f %s",
        temp_value, from_unit, result, to_unit
    )

    print("\n✨ Conversion logged successfully!\n")


if __name__ == "__main__":
    main()
