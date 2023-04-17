# Datastore-Mock
Datastore mock i created for austiblox. i guess


## How to use:
1. To use it first copy the files in the src folder to your desired location in your webserver
2. Then copy the datastore script to your game.
3. Make sure the url of the path of the php file is correct in the lua file aswell!
4. Are you sure your hosting?
5. just kidding lol.
6. Then uhh voila i guess.

## Examples:
 ```
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
