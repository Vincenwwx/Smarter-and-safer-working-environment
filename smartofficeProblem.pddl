(define (problem smartoffice)
(:domain office)
(:objects
   r - room
   f - fan
   l - light
   h - heater
   b - buzzer
   b1 - buzzer1
   p - person
   m - message)

(:init
   
    
    (off l)
    (at-light l r)
    
    (off1 f)
    (at-fan f r)

    (off2 h)
    (at-heater h r)

    (off3 b)
    (at-buzzer b p)

    (off4 b1 )
    (at-buzzer1 b1 p)
    
    
    ;temperature
    (= (temp_limit) 22)
    (= (temp r) 21.0)
    
    ;humidity
    
    (= (humidity_limit) 60)
    (= (humidity r) 55.0 )
    

    ;light intensity
    (= (lightintensity_limit) 8000)
    (= (lightintensity r) 7000.0)
   
    ; body temperature
    (= (bodytemp_limit) 22)
    (= (bodytemp p) 27.0)

    ;motion
    (= (motion_value) 1)
    (= (motion p) 2)

)
(:goal
    (and
          (comfortable-temperature)
          (brightness-sufficient)
          (bodytempcheck-performed)
          (person-detected)
    ))
)