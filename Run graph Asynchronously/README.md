# Async Nodes Benefits VS Challenges

## Advantages
1. Allow us for independent calculations that occur simultaneously.
2. Saves us time and resources and can really speed up the result that we return to the user.


## Disadvantages
1. State Conflict: Here, parallel nodes that modify the same attribute in the state can potentially override each other's changes, so this will lead to inconsistent and unexpected results and potentially can lead to race conditions and data inconsistencies.2. Debugging asynchronously-functionality is more challenging.

## Best Practice
The best practice for using asynchronous execution of nodes is to isolate the state updates. So each node should write to a different attribute in the state to avoid those conflicts, and this practice helps to maintain data integrity and prevents unintended overwrites of the values.