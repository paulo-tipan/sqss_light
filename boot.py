def send_data(r_db, r_name, r_sid, r_temp, r_humi, r_co2, r_o2, r_lux, r_rk):

    html = 'https://flask-api-5ka3ttedna-df.a.run.app/sqss_data?'
    db = f's_db_name={r_db}'
    name = f'&s_sensor_name={r_name}'
    sid = f'&s_sqss_id={r_sid}'
    temp = f'&s_temp={r_temp}'
    humi = f'&s_humi={r_humi}'
    co2 = f'&s_co2x={r_co2}'
    o2 = f'&s_o2xx={r_o2}'
    lux = f'&s_luxx={r_lux}'
    rk = f'&read_key={r_rk}'
    api_data = html + db + name + sid + temp + humi + co2 + o2 + lux + rk

    return api_data