(define (problem comfort)
(:domain office)
(:objects
   r - room
   f - fan
   p - person
   l - light
   h - heater
   m - message)

(:init
   
    
    (off l)
    (at-light l r p)
    
    (off1 f)
    (at-fan f r p)

    (off2 h)
    (at-heater h r p)
    
    
    ;temperature
    (= (temp_limit) 22)
    (= (temp r) 22)
    
    ;humidity
    
    (= (humidity_limit) 60)
    (= (humidity r) 68 )
    

    ;light intensity
    (= (lightintensity_limit) 1)
    (= (lightintensity r) 0.0)
   
   

)
(:goal
    (and
          (comfortable-temperature)
          (brightness-sufficient)
    ))
)