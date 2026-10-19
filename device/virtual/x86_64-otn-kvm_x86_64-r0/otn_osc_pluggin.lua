-- KEYS - rif IDs
-- ARGV[1] - counters db index
-- ARGV[2] - counters table name
-- ARGV[3] - poll time interval
-- return log

local function convertToSigned(unsigned)
  local INT32_MAX = 2^31 - 1
  if unsigned <= INT32_MAX then
    return unsigned
  else
    return unsigned - 2^32
  end
end

local function strValuePro(str, div)
  local v = tonumber(str)
  if not v then return "0" end
  v = convertToSigned(v)
  return tostring(v / div)
end

local DIV = 100

local function scale(v)
  return strValuePro(v, DIV)
end

local logtable = {}

local function logit(msg)
  logtable[#logtable+1] = tostring(msg)
end

local counters_db = ARGV[1]
local counters_table_name = ARGV[2]
local state_db = "6"
local vid_table_name = "COUNTERS_OTN_OSC_NAME_MAP"
local state_table_name = "OTN_OSC_TABLE"

-- {counter attribute, state field, transform fn, default value for first creation}
local specs = {
  {'SAI_OTN_OSC_ATTR_INPUT_POWER',       'input-power',        scale, '-60'},
  {'SAI_OTN_OSC_ATTR_OUTPUT_POWER',      'output-power',       scale, '-60'},
  {'SAI_OTN_OSC_ATTR_LASER_BIAS_CURRENT','laser-bias-current', scale, '0'},
  {'SAI_OTN_OSC_ATTR_OUTPUT_FREQUENCY',  'output-frequency',   nil,   '0'},
}

-- attribute name list for a single HMGET, and the default field/value list
local attrs = {}
local defaults = {}
for i, s in ipairs(specs) do
  attrs[i] = s[1]
  if s[4] then
    defaults[#defaults+1] = s[2]
    defaults[#defaults+1] = s[4]
  end
end

-- Phase 1: read counters, build per-object update lists.
-- Attributes that are missing from COUNTERS are simply left out of the
-- field list, so HMSET will not touch the previous value in STATE_DB.
local updates = {}

redis.call('SELECT', counters_db)
for i = 1, #KEYS do
  local vid = KEYS[i]
  local obj_name = redis.call('HGET', vid_table_name, vid)
  if obj_name then
    local counter_key = counters_table_name .. ':' .. vid
    local vals = redis.call('HMGET', counter_key, unpack(attrs))

    local fields = {}
    for j, s in ipairs(specs) do
      local v = vals[j]
      if v then                     -- missing fields come back as false
        local fn = s[3]
        fields[#fields+1] = s[2]
        fields[#fields+1] = fn and fn(v) or v
      end
    end

    if #fields > 0 then
      updates[#updates+1] = {obj_name, fields}
    else
      logit("No counters for " .. obj_name)
    end
  else
    logit("No mapping for vid=" .. vid)
  end
end

-- Phase 2: write STATE_DB once
redis.call('SELECT', state_db)
for _, u in ipairs(updates) do
  local state_key = state_table_name .. '|' .. u[1]

  -- seed defaults only when the entry does not exist yet, so consumers
  -- never see a half-populated hash on first poll
  if redis.call('EXISTS', state_key) == 0 then
    redis.call('HMSET', state_key, unpack(defaults))
  end

  redis.call('HMSET', state_key, unpack(u[2]))
  logit("Updated " .. u[1])
end

return logtable
