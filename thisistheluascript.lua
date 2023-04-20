local HttpService = game:GetService("HttpService")
local API = {}
local MT = {}

-----------------------------------------------------------------------------------------------------------

-- API:

function API:GetDataStore(name, scope)
    assert(type(name) == "string", "DataStore name must be a string; got " .. type(name))
    assert(type(scope) == "string" or scope == nil, "DataStore scope must be a string; got " .. type(scope))
    scope = (scope or "global")
    if (allStores[scope] and allStores[scope][name]) then
        return allStores[scope][name]
    end
    local d = {}
    function d:SetAsync(k, v)
        assert(v ~= nil, "Value cannot be nil")
        local success, result = pcall(function()
            local payload = {
                name = name,
                scope = scope,
                key = k,
                value = v
            }
            local response = HttpService:RequestAsync({
                Url = "https://example.com/save_data", -- Replace with your server's URL
                Method = "POST",
                Headers = {
                    ["Content-Type"] = "application/json"
                },
                Body = HttpService:JSONEncode(payload)
            })
            return response.Success and HttpService:JSONDecode(response.Body) or nil
        end)
        if not success then
            error("Failed to set data: " .. result)
        end
    end
    function d:UpdateAsync(k, func)
        local oldValue = self:GetAsync(k)
        local v = func(oldValue)
        assert(v ~= nil, "Value cannot be nil")
        self:SetAsync(k, v)
    end
    function d:GetAsync(k)
        local success, result = pcall(function()
            local payload = {
                name = name,
                scope = scope,
                key = k
            }
            local response = HttpService:RequestAsync({
                Url = "https://example.com/get_data", -- Replace with your server's URL
                Method = "POST",
                Headers = {
                    ["Content-Type"] = "application/json"
                },
                Body = HttpService:JSONEncode(payload)
            })
            return response.Success and HttpService:JSONDecode(response.Body) or nil
        end)
        if not success then
            error("Failed to get data: " .. result)
        end
        return result and result.value or nil
    end
    function d:IncrementAsync(k, delta)
        if (delta == nil) then delta = 1 end
        assert(type(delta) == "number", "Can only increment numbers")
        local oldValue = self:GetAsync(k)
        self:SetAsync(k, (oldValue or 0) + delta)
    end
    function d:OnUpdate(k, onUpdateFunc)
        error("OnUpdate is not supported when using HttpService")
    end
    if (not allStores[scope]) then
        allStores[scope] = {}
    end
    allStores[scope][name] = d
    return setmetatable(d, MT)
end

function API:GetGlobalDataStore()
    return self:GetDataStore("global", "global")
end

function API:GetOrderedDataStore(name, scope)
    error("GetOrderedDataStore is not supported when using HttpService")
end

-----------------------------------------------------------------------------------------------------------
-- Metatable:

MT.__index = API

return API
