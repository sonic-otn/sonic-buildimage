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
  v = convertToSigned(v)
  return tostring(v / div)
end

local function hex_decode(str)
    return (str:gsub("\\x(%x%x)", function(hex)
        return string.char(tonumber(hex, 16))
    end))
end

local logtable = {}

local function logit(msg)
  logtable[#logtable+1] = tostring(msg)
end

local counters_db = ARGV[1]
local counters_table_name = ARGV[2] 
local state_db = "6"
local vid_table_name = "COUNTERS_OTN_ATTENUATOR_NAME_MAP"
local state_table_name = "OTN_ATTENUATOR_TABLE"

-- Phase 1: read counters
redis.call('SELECT', counters_db)
for i = 1, #KEYS do
  local vid = KEYS[i]
  local obj_name = redis.call('HGET', vid_table_name, vid)
  if obj_name then
    local div = 100
    -- Get new COUNTERS values
    local counter_key = counters_table_name .. ':' .. vid

    local ingress_port = ""
    local val = redis.call('HGET', counter_key, 'SAI_OTN_ATTENUATOR_ATTR_INGRESS_PORT')
    if val then
      ingress_port = hex_decode(val)
    end

    local egress_port = ""
    val = redis.call('HGET', counter_key, 'SAI_OTN_ATTENUATOR_ATTR_EGRESS_PORT')
    if val then
      egress_port = hex_decode(val)
    end

    local actual_att = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_ATTENUATOR_ATTR_ACTUAL_ATTENUATION')
    if val then
      actual_att = strValuePro(val, div)
    end

    local output_power = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_ATTENUATOR_ATTR_OUTPUT_POWER_TOTAL')
    if val then
      output_power = strValuePro(val, div)
    end

    local return_loss = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_ATTENUATOR_ATTR_OPTICAL_RETURN_LOSS')
    if val then
      return_loss = strValuePro(val, div)
    end

    -- switch to state DB and update
    redis.call('SELECT', state_db)
    redis.call('HMSET', state_table_name .. '|' .. obj_name,
               'ingress-port', ingress_port,
               'egress-port', egress_port,
               'actual-attenuation', actual_att,
               'output-power-total', output_power,
               'optical-return-loss', return_loss)
 
    -- switch back for next iteration
    redis.call('SELECT', counters_db)

    logit("Updated " .. obj_name)
  else
    logit("No mapping for vid=" .. vid)
  end
end

return logtable
