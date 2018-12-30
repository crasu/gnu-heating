t = 0 
RESET = 3
TIMER = 4
interval = 500

function set(st_reset, st_timer)
    gpio.write(RESET, st_reset)
    gpio.write(TIMER, st_timer)
end


function alarm()
    print("Switching time " .. t)
    if t == 0 then
        set(gpio.LOW, gpio.LOW)
        print("getting new adr")
    elseif t == 5 then
        set(gpio.LOW, gpio.HIGH)
    elseif t == 15 then
        set(gpio.HIGH, gpio.HIGH)
    elseif t == 20 then
        set(gpio.LOW, gpio.HIGH)
    elseif t == 25 then
        set(gpio.LOW, gpio.LOW)
    elseif t == 30 then
        set(gpio.HIGH, gpio.LOW)
    elseif t == 35 then
        set(gpio.LOW, gpio.LOW)
        print("inital reset")
    elseif t >= 200 and t % 200 == 0 then
        set(gpio.LOW, gpio.HIGH)
    elseif t >= 300 and t % 200 == 100 then
        set(gpio.LOW, gpio.LOW)
        print("timer pressed")
    elseif t>= 3600 then
        interval=(interval+1)
    end
    t=(t+5)%3000
    tmr.alarm(0, interval, tmr.ALARM_SINGLE, alarm)
end

tmr.alarm(0, 750, tmr.ALARM_SINGLE, alarm)

