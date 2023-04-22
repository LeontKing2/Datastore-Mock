local HttpService = game:GetService("HttpService")
local API = {}
local MT = {}

-----------------------------------------------------------------------------------------------------------
-- API:

function API:GetDataStore(name, scope)
   assert(type(name) == "string", "DataStore name must be a string; got " .. type(name))
   assert(type(scope) == "string" or scope == nil, "DataStore scope must be a string; got " .. type(scope))
   scope = (scope or "global")
   local data = {}
   local d = {}
   function d:SetAsync(k, v)
      assert(v ~= nil, "Value cannot be nil")
      data[k] = v
      self:_SendDataToServer(name, scope, k, v)
   end
   function d:UpdateAsync(k, func)
      local v = func(data[k])
      assert(v ~= nil, "Value cannot be nil")
      data[k] = v
      self:_SendDataToServer(name, scope, k, v)
   end
   function d:GetAsync(k)
      if data[k] ~= nil then
         return data[k]
      else
         local response = self:_GetDataFromServer(name, scope, k)
         if response and response.success then
            data[k] = response.value
            return response.value
         else
            return nil
         end
      end
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
   return d
end

function API:GetGlobalDataStore()
   return self:GetDataStore("global", "global")
end

function API:_SendDataToServer(storeName, storeScope, key, value)
   local payload = {
      storeName = storeName,
      storeScope = storeScope,
      key = key,
      value = value
   }
   local success, response = pcall(function()
   return HttpService:PostAsync("https://your-server-url.com/save", HttpService:JSONEncode(payload))
   end)
   if success then
      local decodedResponse = HttpService:JSONDecode(response)
      if decodedResponse and decodedResponse.success then
         return true
      else
         error("Failed to send data to server: " .. (decodedResponse and decodedResponse.error or "Unknown error"))
      end
   else
      error("Failed to send data to server: " .. response)
   end
end

function API:_GetDataFromServer(storeName, storeScope, key)
   local payload = {
      storeName = storeName,
      storeScope = storeScope,
      key = key
   }
   local success, response = pcall(function()
   return HttpService:PostAsync("https://your-server-url.com/load", HttpService:JSONEncode(payload))
   end)
   if success then
      local decodedResponse = HttpService:JSONDecode(response)
      if decodedResponse and decodedResponse.success then
         return decodedResponse
      else
         error("Failed to get data from server: " .. (decodedResponse and decodedResponse.error or "Unknown error"))
      end
   else
      error("Failed to get data from server: " .. response)
   end
end

-- Metatable:

function MT:__index(k)
   return self:GetAsync(k)
end

function MT:__newindex(k, v)
   self:SetAsync(k, v)
end

function MT:__call(k, v)
   if type(k) == "function" then
      k(self)
   elseif type(v) == "function" then
      v(self)
   end
end

-- DataStore Class:

local DataStore = {}
DataStore.__index = DataStore

function DataStore.new(name, scope)
   local self = setmetatable({}, DataStore)
   self.api = setmetatable({}, MT)
   self.api._GetDataFromServer = API._GetDataFromServer
   self.api._SendDataToServer = API._SendDataToServer
   self.api.GetGlobalDataStore = API.GetGlobalDataStore
   self.api.GetDataStore = API.GetDataStore
   self.api[name] = self.api:GetDataStore(name, scope)
   return self
end

-- Return API:

return DataStore