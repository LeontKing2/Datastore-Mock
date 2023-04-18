local HttpService = game:GetService("HttpService")
local API = {}

function API:GetDataStore(name, scope)
    assert(type(name) == "string", "DataStore name must be a string; got " .. type(name))
    assert(type(scope) == "string" or scope == nil, "DataStore scope must be a string; got " .. type(scope))
    scope = (scope or "global")
    local dataStoreUrl = "https://abhidjt.tk/datastore/" .. scope .. "/" .. name
    local dataStore = {}
    function dataStore:SetAsync(key, value)
        assert(value ~= nil, "Value cannot be nil")
        local success, result = pcall(HttpService.PostAsync, HttpService, dataStoreUrl .. "/" .. key, HttpService:JSONEncode(value))
        if not success then
            error("Failed to save data to server: " .. result)
        end
    end
    function dataStore:GetAsync(key)
        local success, result = pcall(HttpService.GetAsync, HttpService, dataStoreUrl .. "/" .. key)
        if success and result ~= "" then
            return HttpService:JSONDecode(result)
        end
    end
    function dataStore:UpdateAsync(key, updateFunc)
        local oldValue = self:GetAsync(key)
        local newValue = updateFunc(oldValue)
        self:SetAsync(key, newValue)
    end
    function dataStore:IncrementAsync(key, delta)
        self:UpdateAsync(key, function(oldValue)
            if oldValue == nil then
                oldValue = 0
            end
            assert(type(oldValue) == "number", "Value must be a number")
            assert(type(delta) == "number", "Delta must be a number")
            return oldValue + delta
        end)
    end
    return dataStore
end

function API:GetGlobalDataStore()
    return self:GetDataStore("global", "global")
end

function API:GetOrderedDataStore(name, scope)
    error("OrderedDataStore is not supported in this implementation")
end

return API
