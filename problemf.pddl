(define (problem Smart-Safety)
(:domain office)
(:objects
   r1 - room
   l1 - light
   f1 - fan
  
   m1 - message)
(:init
   
    
    (off1 l1)
    (at-light l1 r1)
    
    (off2 f1)
    (at-fan f1 r1)
    
    ;temporarily return values for sensor but actually the sensor values must be fed from mqtt subscriber 
    
    ;temperature
    (= (temp_limit) 22)
    (= (temp r1) 24.0)
    
    ;humidity
    (= (humidity_limit) 60)
    (= (humidity r1) 64.0 )
    

    

    ;light intensity
    (= (light_limit) 10000)
    (= (light r1) 9000.0)
    

)
(:goal
    (and
    
          
          (comfortable-temp)
          (light-sufficient)
          ))
)

