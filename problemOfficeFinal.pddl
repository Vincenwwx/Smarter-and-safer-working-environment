(define (problem Smart-Safety)
(:domain office)
(:objects
   r1 - room
   l1 - light
   f1 - fan
   b1 - buzzer1
   b2 - buzzer2
   p1 - person1
   p2 - person2
   m1 - message)
   
(:init
   
   
   
    (off b1)
    (at-buzzer1 b1 p1)
   
    (off0 b2)
    (at-buzzer2 b2 p2)
   
    (off1 l1)
    (at-light l1 r1)
   
    (off2 f1)
    (at-fan f1 r1)
   
    ;body temperature
    (= (bodytemp_limit) 99 )
    (= (bodytemp p2) 98.0)
   
    ;temperature
    (= (temp_limit) 22)
    (= (temp r1) 24.0)
   
    ;humidity
    (= (humidity_limit) 60)
    (= (humidity r1) 64.0 )
   

    ;light intensity
    (= (light_limit) 10000)
    (= (light r1) 10000.0)
   

)

(:goal
    (and
   
         
         (employee-allowed)
          (employee-denied)
          (comfortable-temp)
          (light-sufficient)
         
          ))
)
