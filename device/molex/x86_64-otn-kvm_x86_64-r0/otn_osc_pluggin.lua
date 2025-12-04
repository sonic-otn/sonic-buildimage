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

local logtable = {}

local function logit(msg)
  logtable[#logtable+1] = tostring(msg)
end

local counters_db = ARGV[1]
local counters_table_name = ARGV[2] 
local state_db = "6"
local vid_table_name = "COUNTERS_OTN_OSC_NAME_MAP"
local state_table_name = "OTN_OSC_TABLE"


-- Phase 1: read counters
redis.call('SELECT', counters_db)
for i = 1, #KEYS do
  local vid = KEYS[i]
  local obj_name = redis.call('HGET', vid_table_name, vid)
  if obj_name then
    local div = 100
    -- Get new COUNTERS values
    local counter_key = counters_table_name .. ':' .. vid

    local input_power = "-60"
    local val = redis.call('HGET', counter_key, 'SAI_OTN_OSC_ATTR_INPUT_POWER')
    if val then
      input_power = strValuePro(val, div)
    end

    local output_power = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OSC_ATTR_OUTPUT_POWER')
    if val then
      output_power = strValuePro(val, div)
    end

    local laser_current = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OSC_ATTR_LASER_BIAS_CURRENT')
    if val then
      laser_current = strValuePro(val, div)
    end

    local output_frequency = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OSC_ATTR_OUTPUT_FREQUENCY')
    if val then
      output_frequency = val
    end

    -- switch to state DB and update
    redis.call('SELECT', state_db)
    redis.call('HMSET', state_table_name .. '|' .. obj_name,
               'input-power', input_power,
               'output-power', output_power,
               'laser-bias-current', laser_current,
               'output-frequency', output_frequency)

    -- switch back for next iteration
    redis.call('SELECT', counters_db)

    logit("Updated " .. obj_name)
  else
    logit("No mapping for vid=" .. vid)
  end
end

return logtable
