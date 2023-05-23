-- CustomDatastoreService.lua

local HttpService = game:GetService("HttpService")
local DatastoreService = {}

local API_URL = "https://your-api-url.com/datastore" -- Replace with your API endpoint

function DatastoreService:GetAsync(gameId, key, defaultValue)
    local url = API_URL .. "/" .. gameId .. "/" .. key
    local response = HttpService:GetAsync(url)
    local decodedResponse = HttpService:JSONDecode(response)
    if decodedResponse ~= nil then
        return decodedResponse
    else
        return defaultValue
    end
end

function DatastoreService:SetAsync(gameId, key, value)
    local url = API_URL .. "/" .. gameId .. "/" .. key
    local encodedData = HttpService:JSONEncode(value)
    HttpService:PostAsync(url, encodedData)
end

function DatastoreService:RemoveAsync(gameId, key)
    local url = API_URL .. "/" .. gameId .. "/" .. key
    HttpService:RequestAsync({Url = url, Method = "DELETE"})
end

return DatastoreService
