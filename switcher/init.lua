gpio.mode(3, gpio.OUTPUT)
gpio.mode(4, gpio.OUTPUT)
gpio.write(3, gpio.LOW)
gpio.write(4, gpio.LOW)

print("*** Starting in 3 secs ***")
tmr.alarm(0, 3000, 0, function()
   print("Executing ...")
   dofile("switcher.lua")
end)

