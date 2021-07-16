(define (problem comfort)
(:domain office)
(:objects
   r - room
   f - fan
   l - light
   h - humidifier
   m - message)

(:init
   
    
    (off l)
    (at-light l r)
    
    (off1 f)
    (at-fan f r)

    (off2 h)
    (at-humidifier h r)
     
    
    ;presence of employee
    (= (occupy_limit) 1)
    (= (occupy r) 1)


    ;temperature
    (= (temp_limit) 23)
    (= (temp r) 26.0)
    
    ;temperature
    (= (temp1_limit) 18)
    (= (temp r) 26.0)

    ;humidity
    
    (= (humidity_limit) 70)
    (= (humidity r) 71.0 )
    

    ;light intensity
    (= (lightintensity_limit) 1)
    (= (lightintensity r) 1)
   
   

)
(:goal
    (and
          
         (comfortable-light)
          (comfortable-temperature)
          (comfortable-humidity)
          
    ))
)