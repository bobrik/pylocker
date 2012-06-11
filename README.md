pylocker - python client for [locker](https://github.com/bobrik/locker) lock server
===========================

Allows to lock common resources across servers with sub-second precision in python.

## Installation

Check out [locker server](https://github.com/bobrik/locker) page for server installation instructions.

Clone this repository to whatever place you keep your python modules.

## Usage


```python
from pylocker import Locker

# create locker server connection
locker = Locker("127.0.0.1", 4545)

# create lock object with some nice name
lock = locker.create_lock("fuu")
# acquire lock, wait for it for 500ms if it's taken
lock.acquire(500, 200)
# do whatever you need for up to 200ms
# and release lock
lock.release()
```

## API

* Importing:

    ```python
    from pylocker import Locker
    ```

* New connection:

    ```python
    locker = Locker("127.0.0.1", 4545)
    ```

* Lock creation:

    ```python
    lock = locker.create_lock(name)
    ```

* Acquiring lock:

    ```python
    lock.acquire(wait, timeout)
    ```

    * `wait` - max time to wait for lock (in milliseconds).
    * `timeout` - max work time before `release` call or auto-release by timeout (in milliseconds).

* Releasing lock:

    ```python
    lock.release(panic = False)
    ```

If `panic = True` then `LostLockException` will be raised if time between `acquire` and `release` was more than `timeout`.

## Usages:

* [@unfollowr](http://unfollower.name/) - twitter bot to track people who unfollowed you
