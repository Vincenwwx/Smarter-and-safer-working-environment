(define (problem comfort)
(:domain office)
(:objects
   r - room
   f - fan
   l - light
   h - heater
   m - message)

(:init
   
    
    (off l)
    (at-light l r)
    
    (off1 f)
    (at-fan f r)

    (off2 h)
    (at-heater h r)
    
    
    ;temperature
    (= (temp_limit) 22)
    (= (temp r) 12.22)
    
    ;humidity
    (= (humidity_limit) 60)
    (= (humidity r) 88.1)
    

    ;light intensity
    (= (lightintensity_limit) 1)
    (= (lightintensity r) 2)
   
   

)
(:goal
    (and
          (comfortable-temperature)
          (brightness-sufficient)
    ))
)