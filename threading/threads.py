import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_URL = "https://jsonplaceholder.typicode.com/users/{}"

# Fetch a single user by ID


def fetch_user(user_id):
    response = requests.get(USER_URL.format(user_id))
    return response.json() if response.status_code == 200 else None


# Sequential fetching


def fetch_users_sequential():
    users = []
    for user_id in range(1, 11):
        user = fetch_user(user_id)
        users.append(user)
    return users


# ThreadPoolExecutor-based threaded fetching


def fetch_users_threadpool():
    users = [None] * 10
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_idx = {
            executor.submit(fetch_user, user_id): idx
            for idx, user_id in enumerate(range(1, 11))
        }
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            users[idx] = future.result()
    return users


if __name__ == "__main__":
    print("Sequential fetch:")
    start = time.time()
    users_seq = fetch_users_sequential()
    print(f"Fetched {len(users_seq)} users in {time.time() - start:.2f} seconds\n")

    print("ThreadPoolExecutor fetch:")
    start = time.time()
    users_thr = fetch_users_threadpool()
    print(f"Fetched {len(users_thr)} users in {time.time() - start:.2f} seconds")
