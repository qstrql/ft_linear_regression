import json
import math
import os


def estimate_price(mileage, theta0, theta1):
    """
    Calculate estimated price using linear regression formula.

    estimatePrice(mileage) = θ0 + (θ1 * mileage)
    """
    return theta0 + (theta1 * mileage)


def load_theta():
    """
    Load theta0 and theta1 from the json file.

    If the json file doesn't exist, return (0, 0).
    """
    if not os.path.exists('theta.json'):
        return 0, 0

    with open('theta.json', 'r') as file:
        data = json.load(file)
        return data['theta0'], data['theta1']


def main():
    """Main function with error handling."""
    try:
        theta0, theta1 = load_theta()

        mileage = float(input("Enter a mileage: "))
        if math.isinf(mileage) or math.isnan(mileage):
            print("Error: Number is too large")
            return

        price = estimate_price(mileage, theta0, theta1)
        print(f"Estimated price: {price}")

    except ValueError:
        print("Error: Please enter a valid mileage number")
    except KeyboardInterrupt:
        print("\nProgram interrupted")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
