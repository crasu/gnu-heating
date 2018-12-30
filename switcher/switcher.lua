t = 0 
RESET = 3
TIMER = 4
interval = 400

function set(st_reset, st_timer)
    gpio.write(RESET, st_reset)
    gpio.write(TIMER, st_timer)
end


function alarm()
    print("Switching time " .. t)
    if t == 0 then
        set(gpio.LOW, gpio.LOW)
    elseif t == 500 then
        set(gpio.LOW, gpio.HIGH)
    elseif t == 1500 then
        set(gpio.HIGH, gpio.HIGH)
    elseif t == 2000 then
        set(gpio.LOW, gpio.HIGH)
    elseif t == 2500 then
        set(gpio.LOW, gpio.LOW)
    elseif t == 7000 then
        set(gpio.HIGH, gpio.LOW)
    elseif t == 7500 then
        set(gpio.LOW, gpio.LOW)
        interval=(interval+1)%2000
    end
    t=(t+500)%10000
    tmr.alarm(0, interval, tmr.ALARM_SINGLE, alarm)
end


tmr.alarm(0, 750, tmr.ALARM_SINGLE, alarm)

