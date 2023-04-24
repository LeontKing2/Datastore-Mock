# Datastore-Mock
Datastore mock i created for austiblox. i guess
## Warning! This is for personal use only(by that i mean no other game can connect to your python script unless you host another one with a different port)

## How to use:
1. Start the python script(make sure to install em flask package)
2. Make sure you got the right domain? i am using a nginx proxy so i can use port 443 if i want to while proxying it to localhost.
3. then use the lua script in game????
4. Voila???

## Examples:
 ```
 *// Might be outdated//*
 local DataStore = require(path/to/DataStore) -- Replace with actual path to the datastore script

local globalDataStore = DataStore:GetGlobalDataStore()

-- Set some data
globalDataStore:SetAsync("Hello", "world")
globalDataStore:SetAsync("PlayerCount", 10)

-- Get the data
local hello = globalDataStore:GetAsync("Hello")
local playerCount = globalDataStore:GetAsync("PlayerCount")

print(hello) -- Output: world
print(playerCount) -- Output: 10
 ```
## This is based of off thexkey's repo. thanks