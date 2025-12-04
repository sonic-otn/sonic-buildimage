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
local vid_table_name = "COUNTERS_OTN_OA_NAME_MAP"
local state_table_name = "OTN_OA_TABLE"

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
    local val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_INGRESS_PORT')
    if val then
      ingress_port = hex_decode(val)
    end

    local egress_port = ""
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_EGRESS_PORT')
    if val then
      egress_port = hex_decode(val)
    end

    local actual_gain = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_ACTUAL_GAIN')
    if val then
      actual_gain = strValuePro(val, div)
    end

    local actual_tilt = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_ACTUAL_GAIN_TILT')
    if val then
      actual_tilt = strValuePro(val, div)
    end

    local input_power_total = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_INPUT_POWER_TOTAL')
    if val then
      input_power_total = strValuePro(val, div)
    end

    local input_power_c = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_INPUT_POWER_C_BAND')
    if val then
      input_power_total = strValuePro(val, div)
    end

    local input_power_l = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_INPUT_POWER_L_BAND')
    if val then
      input_power_l = strValuePro(val, div)
    end

    local output_power_total = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_OUTPUT_POWER_TOTAL')
    if val then
      output_power_total = strValuePro(val, div)
    end

    local output_power_c = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_OUTPUT_POWER_C_BAND')
    if val then
      output_power_c = strValuePro(val, div)
    end

    local output_power_l = "-60"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_OUTPUT_POWER_L_BAND')
    if val then
      output_power_l = strValuePro(val, div)
    end

    local laser_current = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_LASER_BIAS_CURRENT')
    if val then
      laser_current = strValuePro(val, div)
    end

    local return_loss = "0"
    val = redis.call('HGET', counter_key, 'SAI_OTN_OA_ATTR_OPTICAL_RETURN_LOSS')
    if val then
      return_loss = strValuePro(val, div)
    end

    -- switch to state DB and update
    redis.call('SELECT', state_db)
    redis.call('HMSET', state_table_name .. '|' .. obj_name,
               'ingress-port', ingress_port,
               'egress-port', egress_port,
               'actual-gain', actual_gain,
               'actual-gain-tilt', actual_tilt,
               'input-power-total', input_power_total,
               'input-power-c-band', input_power_c,
               'input-power-l-band', input_power_l,
               'output-power-total', output_power_total,
               'output-power-c-band', output_power_c,
               'output-power-l-band', output_power_l,
               'laser-bias-current', laser_current,
               'optical-return-loss', return_loss)

    -- switch back for next iteration
    redis.call('SELECT', counters_db)

    logit("Updated " .. obj_name)
  else
    logit("No mapping for vid=" .. vid)
  end
end

return logtable
