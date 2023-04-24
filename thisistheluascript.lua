local DataStoreService = {}
local API = {}
local MT = {}
local HttpService = game:GetService("HttpService")

-----------------------------------------------------------------------------------------------------------

local allStores = {}




-----------------------------------------------------------------------------------------------------------
-- API:

function API:GetDataStore(name, scope)
    assert(type(name) == "string", "DataStore name must be a string; got" .. type(name))
    assert(type(scope) == "string" or scope == nil, "DataStore scope must be a string; got" .. type(scope))
    scope = (scope or "global")
    if (allStores[scope] and allStores[scope][name]) then
        return allStores[scope][name]
    end
    local data = {}
    local d = {}
    local updateListeners = {}
    function d:SetAsync(k, v)
        assert(v ~= nil, "Value cannot be nil")
        data[k] = v
        if (updateListeners[k]) then
            for _,f in pairs(updateListeners[k]) do
                spawn(function() f(v) end)
            end
        end
        -- Send data to HTTP server
        local payload = {key = k, value = v}
        local success, err = pcall(function()
            HttpService:PostAsync("https://example.com/datastore", HttpService:JSONEncode(payload))
        end)
        if not success then
            error("Failed to send data to HTTP server: " .. err)
        end
    end
    function d:UpdateAsync(k, func)
        local v = func(data[k])
        assert(v ~= nil, "Value cannot be nil")
        data[k] = v
        if (updateListeners[k]) then
            for _,f in pairs(updateListeners[k]) do
                spawn(function() f(v) end)
            end
        end
        -- Send data to HTTP server
        local payload = {key = k, value = v}
        local success, err = pcall(function()
            HttpService:PostAsync("https://example.com/datastore", HttpService:JSONEncode(payload))
        end)
        if not success then
            error("Failed to send data to HTTP server: " .. err)
        end
    end
    function d:GetAsync(k)
        return data[k]
    end
    function d:IncrementAsync(k, delta)
        if (delta == nil) then delta = 1 end
        assert(type(delta) == "number", "Can only increment numbers")
        self:UpdateAsync(k, function(num)
            if (num == nil) then
                return num
            end
            assert(type(num) == "number", "Can only increment numbers")
            return (num + delta)
        end)
    end
    function d:OnUpdate(k, onUpdateFunc)
        assert(type(onUpdateFunc) == "function", "Update function argument must be a function")
        if (not updateListeners[k]) then
            updateListeners[k] = {onUpdateFunc}
        else
            table.insert(updateListeners[k], onUpdateFunc)
        end
    end
    if (not allStores[scope]) then
        allStores[scope] = {}
    end
    allStores[scope][name] = d
    return d
end

function API:GetGlobalDataStore()
    return self:GetDataStore("GlobalDataStore", "global")
end
   
   -- Metatable:
   
MT.__index = function(self, key)
if (API[key]) then
   return API[key]
else
   error("Invalid DataStoreService API: " .. key)
   end
end
   
setmetatable(DataStoreService, MT)
   
   -- Return mocked DataStoreService:
   
return DataStoreService