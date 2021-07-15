(define (problem safety)
(:domain office)
(:objects
   b - buzzer
   b1 - buzzer1
   p - person
   m - message)

(:init
   

    (off3 b)
    (at-buzzer b p)

    (off4 b1 )
    (at-buzzer1 b1 p)
    
    ; body temperature
    (= (bodytemp_limit) 22)
    (= (bodytemp p) 27.562)

    ;motion
    (= (motion_value) 1)
    (= (motion p) 0)

)
(:goal
    (and
          (bodytempcheck-performed)
          (person-detected)
    ))
)