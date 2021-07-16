(define (problem comfort)
(:domain office)
(:objects
   r - room
   f - fan
   p - person
   l - light
   h - humidifier
   m - message)

(:init
   
    
    (off l)
    (at-light l r p)
    
    (off1 f)
    (at-fan f r p)

    (off2 h)
    (at-humidifier h r p)
    
    
    ;temperature
    (= (temp_limit) 23)
    (= (temp r) 26.0)
    
    ;temperature
    (= (temp1_limit) 18)
    (= (temp r) 26.0)

    ;humidity
    
    (= (humidity_limit) 70)
    (= (humidity r) 55.0 )
    

    ;light intensity
    (= (lightintensity_limit) 1)
    (= (lightintensity r) 0.0)
   
   

)
(:goal
    (and
          (comfortable-temperature)
          (comfortable-humidity)
          (brightness-sufficient)
    ))
)