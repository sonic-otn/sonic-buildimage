
typedef i32 dapi_status_t

struct dapi_psu_all_t{
1:	i32	abs;
2:	i32	ambient_temp;
3:	i32	primary_temp;
4:	i32	secondary_temp;
5:	i32	vout;
6:	i32	vin;
7:	i32 iout;
8:	i32 iin;
9:	i32	pout;
10:	i32 pin;
11:	i32 fan;
12:	i32 capacity;
13:	string pn;
14:	string sn;
15:	string model_name;
16:	string location;
17: string revision;
18: string date;
}

enum psu_id_e{
	PSU1_ID = 1,
	PSU2_ID,
}

enum psu_abs_e{
	PSU_ABS_IN,
	PSU_ABS_OUT,
	
}

enum led_type_e{
	LED_RED,
	LED_GREEN,
	LED_ORANGE,
	LED_OFF,
	LED_UNKNOW,
}

enum led_value_e{
	LED_OFF,
	LED_ON,
}

enum fan_id_e{
	FAN1_ID = 1,
	FAN2_ID,
	FAN3_ID,
	FAN4_ID,
	FAN5_ID,
}

enum fan_abs_e{
	FAN_ABS_IN,
	FAN_ABS_OUT,
}

enum slot_abs_e{
	SLOT_ABS_IN,
	SLOT_ABS_OUT,
}

enum slot_power_e{
	SLOT_POWER_OFF,
	SLOT_POWER_ON,
}

enum slot_id_e{
	SLOTM_ID,
	SLOT1_ID,
	SLOT2_ID,
	SLOT3_ID,
	SLOT4_ID,
	SLOTX86_ID,
	FAN1_ID,
	FAN2_ID,
	FAN3_ID,
	FAN4_ID,
	FAN5_ID,
}

enum reboot_type_e{
	REBOOT_POWER,
	REBOOT_COLD,
	REBOOT_SOFT,
	REBOOT_ABNORMAL,
	REBOOT_DOG = 0xDD,
	REBOOT_BUTTON = 0xBB,
}

struct dapi_eeprom_all_t{
1:	string slot_type;
2:  string model_name;
3:	string pn;
4:	string sn;
5:	string label;
6:	string hw_version;
7:	string sw_version;
8:	string release_date;
9:	string mac_addr;
}

struct dapi_eeprom_up_t{
1:	string product_name;
2:  string product_number;
3:	string model_name;
4:	string model_date;
5:	string model_revision;
6:	i32 running_time_once;
7:	i32 running_time_total;
8:	string reserved;
}

struct dapi_fan_speed_t{
1:	i32	speed1;
2:	i32	speed2;
}

struct dapi_90120vol_all_t{
1:	i32	vol1;
2:	i32	vol2;
3:	i32	vol3;
4:	i32	vol4;
5:	i32	vol5;
6:	i32	vol6;
7:	i32	vol7;
8:	i32	vol8;
9:	i32	vol9;
10:	i32	vol10;
11:	i32	vol11;
12:	i32	vol12
}

struct dapi_upvol_all_t{
1:	i32	vol1;
2:	i32	vol2;
3:	i32	vol3;
4:	i32	vol4;
5:	i32	vol5;
6:	i32	vol6;
7:	i32	vol7;
8:	i32	vol8;
}

struct dapi_switch_port_stat_t{
1:	i64 in_octets;
2:	i64 in_pkts;
3:	i64 in_unicast_pkts;
4:	i64 in_broadcast_pkts;
5:	i64 in_multicast_pkts;
6:	i64 in_discards;
7:	i64 in_errors;
8:	i64 in_unknown_protos;
9:	i64 in_fcs_errors;
10:	i64 out_octets;
11:	i64 out_pkts;
12:	i64 out_unicast_pkts;
13:	i64 out_broadcast_pkts;
14:	i64 out_multicast_pkts;
15:	i64 out_discards;
16:	i64 out_errors;
17:	i64 carrier_transitions;
18:	i64 lastClear;
}

service dev_dapi_rpc {

	string dapi_get_dev_ver();
	string dapi_get_pcb_ver();
	string dapi_get_bom_ver();
	string dapi_get_sonic_ver();
	// psu api
	i32 dapi_get_psu_abs(1: i8 psu_id);
	i32 dapi_get_psu_ambient_temp(1: i8 psu_id);
	i32 dapi_get_psu_primary_temp(1: i8 psu_id);
	i32 dapi_get_psu_secondary_temp(1: i8 psu_id);
	i32 dapi_get_psu_vout(1: i8 psu_id);
	i32 dapi_get_psu_vin(1: i8 psu_id);
	i32 dapi_get_psu_iout(1: i8 psu_id);
	i32 dapi_get_psu_iin(1: i8 psu_id);
	i32 dapi_get_psu_pout(1: i8 psu_id);
	i32 dapi_get_psu_pin(1: i8 psu_id);
	i32 dapi_get_psu_fan(1: i8 psu_id);
	i32 dapi_get_psu_capacity(1: i8 psu_id);
	string dapi_get_psu_pn(1: i8 psu_id);
	string dapi_get_psu_sn(1: i8 psu_id);
	string dapi_get_psu_model_name(1: i8 psu_id);
	string dapi_get_psu_revision(1: i8 psu_id);
	string dapi_get_psu_location(1: i8 psu_id);	
	string dapi_get_psu_date(1: i8 psu_id);	
	
	dapi_psu_all_t dapi_get_psu_all(1: i8 psu_id);
	
	// fan api
	i8 dapi_get_fan_abs(1: i8 fan_id);
	dapi_status_t dapi_set_fan_enable(1: i8 fan_id);
	dapi_fan_speed_t dapi_get_fan_speed(1: i8 fan_id);
	dapi_status_t dapi_set_fan_speed(1: i8 fan_id, 2: i32 fan_speed);
	i32 dapi_get_fan_temp(1: i8 fan_id);
	dapi_status_t dapi_set_fan_feed_dog();
	dapi_status_t dapi_set_fan_dog_interval(1: i32 fan_dog_interval);
	i32 dapi_get_fan_reg(1: i8 fan_id,2: i32 fan_reg);
	dapi_status_t dapi_set_fan_reg(1: i8 fan_id,2: i32 fan_reg,3: i8 data);
	i32 dapi_get_fan_up_temp(1: i8 fan_id);
	dapi_status_t dapi_set_fan_up_temp(1: i8 fan_id, 2: i32 fan_temp);
	i32 dapi_get_fan_down_temp(1: i8 fan_id);
	dapi_status_t dapi_set_fan_down_temp(1: i8 fan_id, 2: i32 fan_temp);
	
	// dog api
	dapi_status_t dapi_set_dog_feed();
	dapi_status_t dapi_set_dog_enable();
	dapi_status_t dapi_set_dog_disable();
	dapi_status_t dapi_set_dog_interval(1: i32 interval);
	
	// temp&eeprom api
	i32 dapi_get_mainboard_temp();
	i32 dapi_get_cpu_temp();
	i32 dapi_get_x86board_temp();
	i32 dapi_get_slot_temp(1: i8 slot_id);
	
	i32 dapi_boardinfo_eeprom_init(1: i8 slot_id);
	
	string dapi_get_fan_eeprom(1: i8 fan_id, 2: i32 addr, 3: i32 len);
	dapi_status_t dapi_set_fan_eeprom(1: i8 fan_id, 2: i32 addr, 3: i32 len 4: string data);
	string dapi_get_mainboard_eeprom(1: i32 addr, 2: i32 len);
	dapi_status_t dapi_set_mainboard_eeprom(1: i32 addr, 2: i32 len 3: string data);
	dapi_eeprom_up_t dapi_get_x86upboard_eeprom();
	dapi_status_t dapi_set_x86upboard_eeprom(1: dapi_eeprom_up_t info);
	string dapi_get_x86board_eeprom(1: i32 addr, 2: i32 len);
	dapi_status_t dapi_set_x86board_eeprom(1: i32 addr, 2: i32 len 3: string data);
	string dapi_get_slot_eeprom(1: i8 slot_id, 2: i32 addr, 3: i32 len);
	dapi_status_t dapi_set_slot_eeprom(1: i8 slot_id, 2: i32 addr, 3: i32 len 4: string data);
	
	dapi_eeprom_all_t dapi_get_slot_eeprom_all(1: i8 slot_id);
	dapi_status_t dapi_set_slot_eeprom_all(1: i8 slot_id, 2: dapi_eeprom_all_t info);
	string dapi_get_slot_type(1: i8 slot_id);
	dapi_status_t dapi_set_slot_type(1: i8 slot_id, 2:string data);
	string dapi_get_slot_pn(1: i8 slot_id);
	dapi_status_t dapi_set_slot_pn(1: i8 slot_id, 2:string data);
	string dapi_get_slot_sn(1: i8 slot_id);
	dapi_status_t dapi_set_slot_sn(1: i8 slot_id, 2:string data);
	string dapi_get_slot_mac(1: i8 slot_id);
	dapi_status_t dapi_set_slot_mac(1: i8 slot_id, 2:string data);
	string dapi_get_slot_release_date(1: i8 slot_id);
	dapi_status_t dapi_set_slot_release_date(1: i8 slot_id, 2:string data);
	string dapi_get_slot_hw_version(1: i8 slot_id);
	dapi_status_t dapi_set_slot_hw_version(1: i8 slot_id, 2:string data);
	string dapi_get_slot_label(1: i8 slot_id);
	dapi_status_t dapi_set_slot_label(1: i8 slot_id, 2:string data);
	string dapi_get_slot_model_name(1: i8 slot_id);
	dapi_status_t dapi_set_slot_model_name(1: i8 slot_id, 2:string data);
	string dapi_get_slot_sw_version(1: i8 slot_id);
	dapi_status_t dapi_set_slot_sw_version(1: i8 slot_id, 2:string data);
	
	// led api
	i32 dapi_get_led_fan_col(1: i8 fan_id);
	dapi_status_t dapi_set_led_system(1: i8 led_type, 2: i8 led_val);
	dapi_status_t dapi_set_led_fan_col(1: i8 fan_id, 2: i8 led_type);
	dapi_status_t dapi_set_led_fan(1: i8 fan_id, 2: i8 led_type, 3: i8 led_val);
	dapi_status_t dapi_set_led_slot(1: i8 slot_id, 2: i8 led_type, 3: i8 led_val);
	
	// switch api
	dapi_status_t dapi_set_switch_init();
        dapi_status_t dapi_show_switch_info();
	//i8 dapi_get_switch_port_link(1: i8 port_id);
	dapi_switch_port_stat_t dapi_get_switch_port_stat_counter(1: i8 port_id);
	dapi_status_t dapi_set_switch_debug_eth();
	dapi_status_t dapi_set_port_default_vlan(1: i32 port_id, 2: i32 default_vlan);
    	dapi_status_t dapi_dev_port_link_set(1: i32 port_num,2: i8 link_flag);
    	i8 dapi_dev_port_link_get(1: i32 port_num);
    
	// fpga api
	string dapi_get_fpga_ver(1: i32 fpga_id);
	//string dapi_get_fpga_data(1: i32 fpga_id);
	//dapi_status_t dapi_upgrade_fpga(1: i32 fpga_id,2:string file_path);
	dapi_upvol_all_t dapi_get_fpga_monitor_vol();
	i32 dapi_get_slot_abs(1: i8 slot_id);
	dapi_status_t dapi_set_uart_sel(1: i8 slot_id);
	i32 dapi_get_rebootype();
	dapi_status_t dapi_set_rebootype(1: i32 type);
	string dapi_get_fpga_down_reg(1: i32 addr, 2: i32 len, 3: i32 delay);
	dapi_status_t dapi_set_fpga_down_reg(1: i32 addr, 2: string pdata, 3: i32 len);
	string dapi_get_fpga_up_reg(1: i32 addr, 2: i32 len);
	dapi_status_t dapi_set_fpga_up_reg(1: i32 addr, 2: string pdata, 3: i32 len);
	
	// power ucd90120 api
	string dapi_read_power_reg(1: i8 slot_id, 2: i32 reg, 3: i32 len);
	dapi_status_t dapi_write_power_reg(1: i8 slot_id, 2: i32 reg, 3: i32 len, 4: string data);
	dapi_status_t dapi_set_power_ctl(1: i8 slot_id, 2: i32 state);
	i32 dapi_get_power_faultlog_number(1: i8 slot_id);
	string dapi_get_power_faultlog_detail(1: i8 slot_id, 2: i32 total, 3: i32 index);
	dapi_status_t dapi_reset_cpu_power();
	i32 dapi_get_power_status(1: i8 slot_id);
	dapi_90120vol_all_t dapi_get_power_vol(1: i8 slot_id);
	dapi_status_t dapi_set_power_time(1: i8 slot_id);
	dapi_status_t dapi_reboot();
	dapi_status_t dapi_restart_swss();
	string dapi_get_power_ver(1: i8 slot_id);
	
	//cpu&mem
	i32 dapi_get_cpu_ratio();
	i32 dapi_get_mem_ratio();
	i32 dapi_get_mem_use();
	i32 dapi_get_mem_free();
	
	//other
	dapi_status_t dapi_upgrade_fpga(1: i8 fpga_type, 2: i8 chip, 3: string file_path);
	i32 dapi_get_upgrade_fpga_status();
	dapi_status_t dapi_set_fpga_reboot(1: i8 fpga_type, 2: i8 reboot_type);
	dapi_status_t dapi_upgrade_bios(1: i32 bios_id, 2: string file_path);
	string dapi_uart_key_get();
	dapi_status_t dapi_uart_key_set(1:string uart_key);
	string dapi_i2cbus_get(1: i8 bus_id, 2: i8 channel, 3: i32 addr, 4: i32 reg, 5: i32 len);
	dapi_status_t dapi_i2cbus_set(1: i8 bus_id, 2: i8 channel, 3: i32 addr, 4: i32 reg, 5: i32 data);
	dapi_status_t dapi_ft4222soft_reset(1: i8 ft4222_id);
	dapi_status_t dapi_ft4222bus_reset(1: i8 ft4222_id);
	string dapi_fpga_get(1: i16 cs1, 2: i16 cs2, 4: i32 reg, 5: i32 len);
	dapi_status_t dapi_fpga_set(1: i16 cs1, 2: i16 cs2, 4: i32 reg, 5: i32 data);
	string dapi_upfpga_get(1: i32 addr, 2: i32 len);
	dapi_status_t dapi_upfpga_set(1: i32 addr, 2: i32 len, 3:i32 data);
	dapi_status_t dapi_recover_default_config(1: i8 slot_id, 2: string data);
        dapi_status_t dapi_dev_vlan_member_tag_set(1: i16 vlan_id, 2: i32 port_num, 3: i8 tag_flag);
}