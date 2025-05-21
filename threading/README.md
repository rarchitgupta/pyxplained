# Python Threading Demo: Sequential vs. ThreadPoolExecutor

This demo illustrates the difference between sequential and concurrent (threaded) execution in Python when fetching data from an external API. It is designed to help learners understand both the conceptual and syntactic aspects of threading in Python.

---

## Problem Statement

Fetch user data for users 1 to 10 from the public API:
```
https://jsonplaceholder.typicode.com/users/{id}
```
We want to compare the time taken to fetch this data sequentially (one after another) vs. concurrently (in parallel) using Python's modern threading tools.

---

## Key Concepts

### 1. Sequential Execution
- Each API call is made one after the other.
- The next call waits for the previous one to finish.
- **Downside:** If each call takes 0.5 seconds, 10 calls will take about 5 seconds.

### 2. Concurrent Execution with ThreadPoolExecutor
- Multiple API calls are made in parallel, each in its own thread.
- The total time is roughly equal to the slowest single call (plus a little overhead).
- **Benefit:** Waiting for network responses (I/O) is done in parallel, greatly reducing total time.

### 3. ThreadPoolExecutor (from concurrent.futures)
- A high-level API to manage a pool of threads.
- Handles thread creation, scheduling, and result collection.
- Recommended for most I/O-bound concurrency tasks in Python.

---

## Code Walkthrough

### Fetching a Single User
```python
def fetch_user(user_id):
    response = requests.get(USER_URL.format(user_id))
    return response.json() if response.status_code == 200 else None
```
- Makes an HTTP GET request for a specific user.
- Returns the user data as a Python dictionary if successful.

### Sequential Fetching
```python
def fetch_users_sequential():
    users = []
    for user_id in range(1, 11):
        user = fetch_user(user_id)
        users.append(user)
    return users
```
- Loops from user 1 to 10, fetching each one after the previous finishes.
- Appends each result to a list.

### Threaded Fetching with ThreadPoolExecutor
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

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
```
- `ThreadPoolExecutor(max_workers=10)` creates a pool of 10 threads.
- `executor.submit(fetch_user, user_id)` schedules a fetch for each user in a separate thread.
- `as_completed(future_to_idx)` yields futures as they finish, so results can be collected as soon as they're ready.
- Results are stored in the correct order using the `future_to_idx` mapping.

---

## Timing the Difference
```python
import time

start = time.time()
users_seq = fetch_users_sequential()
print(f"Fetched {len(users_seq)} users in {time.time() - start:.2f} seconds")

start = time.time()
users_thr = fetch_users_threadpool()
print(f"Fetched {len(users_thr)} users in {time.time() - start:.2f} seconds")
```
- Measures and prints the time taken for both methods.
- You should see a significant speedup with ThreadPoolExecutor!

---

## When to Use Threading
- Threading is best for I/O-bound tasks (like network requests, disk reads/writes).
- For CPU-bound tasks (heavy computation), use multiprocessing instead.

---

## Further Reading
- [concurrent.futures.ThreadPoolExecutor docs](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)
- [Real Python: ThreadPoolExecutor](https://realpython.com/python-concurrency/)
- [Official requests library docs](https://docs.python-requests.org/en/latest/)

---

Feel free to run and modify the code in `threads.py` to experiment further!
