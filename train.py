import csv
import json


LEARNING_RATE = 0.1
ITERATIONS = 1000


def estimate_price(mileage, theta0, theta1):
    """
    estimatePrice(mileage) = theta0 + (theta1 * mileage)
    """
    return theta0 + (theta1 * mileage)


def load_data(filename):
    """
    Read dataset from data.csv file.
    Returns two lists: mileages and prices
    """
    mileages = []
    prices = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mileages.append(float(row['km']))
            prices.append(float(row['price']))

    return mileages, prices


def normalize(data):
    """
    Normalize data to range [0, 1] using min-max normalization.
    Returns normalized data, min value, and max value.
    """
    min_val = min(data)
    max_val = max(data)
    range_val = max_val - min_val

    if range_val == 0:
        return [0] * len(data), min_val, max_val

    normalized = [(x - min_val) / range_val for x in data]
    return normalized, min_val, max_val


def denormalize_theta(theta0, theta1, km_min, km_max, price_min, price_max):
    """
    Convert normalized theta values back to original scale.
    """
    km_range = km_max - km_min
    price_range = price_max - price_min

    if km_range == 0:
        return price_min, 0

    denorm_theta1 = theta1 * (price_range / km_range)
    denorm_theta0 = price_min + (theta0 * price_range)-(denorm_theta1 * km_min)

    return denorm_theta0, denorm_theta1


def train(mileages, prices):
    """
    Train the linear regression model using gradient descent.

    Formulas:
    tmpθ0 = learningRate * (1/m) * Σ(estimatePrice(mileage[i]) - price[i])
    tmpθ1 = learningRate * (1/m) *
            Σ((estimatePrice(mileage[i]) - price[i]) * mileage[i])
    """
    norm_mileages, km_min, km_max = normalize(mileages)
    norm_prices, price_min, price_max = normalize(prices)

    m = len(norm_mileages)

    theta0 = 0.0
    theta1 = 0.0

    for iteration in range(ITERATIONS):
        sum_theta0 = 0.0
        sum_theta1 = 0.0

        for i in range(m):
            estimated = estimate_price(norm_mileages[i], theta0, theta1)
            error = estimated - norm_prices[i]

            sum_theta0 += error
            sum_theta1 += error * norm_mileages[i]

        tmp_theta0 = LEARNING_RATE * (1.0 / m) * sum_theta0
        tmp_theta1 = LEARNING_RATE * (1.0 / m) * sum_theta1

        theta0 = theta0 - tmp_theta0
        theta1 = theta1 - tmp_theta1

    theta0, theta1 = denormalize_theta(
        theta0, theta1, km_min, km_max, price_min, price_max
    )

    return theta0, theta1


def save_theta(theta0, theta1):
    """
    Save theta0 and theta1 to a JSON file.
    """
    data = {
        'theta0': theta0,
        'theta1': theta1
    }

    with open('theta.json', 'w') as f:
        json.dump(data, f, indent=2)


def main():
    """Main function to train the model and save the theta values."""
    try:
        mileages, prices = load_data('data.csv')
        theta0, theta1 = train(mileages, prices)
        save_theta(theta0, theta1)
        print("Theta values saved!")
        print(f"theta0 = {theta0}")
        print(f"theta1 = {theta1}")
    except FileNotFoundError:
        print("Error: data.csv file not found")
    except KeyError as e:
        print(f"Error: Missing column in CSV - {e}")
    except ValueError as e:
        print(f"Error: Invalid data in CSV - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
