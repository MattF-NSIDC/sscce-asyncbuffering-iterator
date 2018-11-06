# Goal

An asynchronous iterator which can repeatedly fetch new results while iterating
over the results received.

The real-world API that we're mocking out gives us results in chunks of 2,000.
Python should be able to parse all 2,000 while waiting for the next 2,000.

# Example

## Iterating over results (public API)

    async for item in AsyncGetData():
      # do something

## Not what we want, but what we have

    $ python test.py 
    Buffer looks low (deque([])). Getting data (takes 1 seconds)...
    Received [0, 1, 2, 3, 4], added to buffer: deque([0, 1, 2, 3, 4])
      Got data: 0
      Got data: 1
      Got data: 2
    Buffer looks low (deque([3, 4])). Getting data (takes 1 seconds)...
    Received [5, 6, 7, 8, 9], added to buffer: deque([3, 4, 5, 6, 7, 8, 9])
      Got data: 3
      Got data: 4
      Got data: 5
      Got data: 6
      Got data: 7
    Buffer looks low (deque([8, 9])). Getting data (takes 1 seconds)...
    Received [10, 11, 12, 13, 14], added to buffer: deque([8, 9, 10, 11, 12, 13, 14])
      Got data: 8
      Got data: 9
      Got data: 10
      Got data: 11
      Got data: 12
    Buffer looks low (deque([13, 14])). Getting data (takes 1 seconds)...
    No more pages of results available.
    Received [], added to buffer: deque([13, 14])
      Got data: 13
      Got data: 14


## What we want

    $ python test.py 
    Buffer looks low (deque([])). Getting data (takes 1 seconds)...
    Received [0, 1, 2, 3, 4], added to buffer: deque([0, 1, 2, 3, 4])
      Got data: 0
      Got data: 1
      Got data: 2
    Buffer looks low (deque([3, 4])). Getting data (takes 1 seconds)...
      Got data: 3
      Got data: 4
    Received [5, 6, 7, 8, 9], added to buffer: deque([5, 6, 7, 8, 9])
      Got data: 5
      Got data: 6
      Got data: 7
    Buffer looks low (deque([8, 9])). Getting data (takes 1 seconds)...
      Got data: 8
      Got data: 9
    Received [10, 11, 12, 13, 14], added to buffer: deque([10, 11, 12, 13, 14])
      Got data: 10
      Got data: 11
      Got data: 12
    Buffer looks low (deque([13, 14])). Getting data (takes 1 seconds)...
      Got data: 13
      Got data: 14
    No more pages of results available.
    Received [], added to buffer: deque([])
