(define (problem safety)

(:domain office)

(:objects
    b - buzzer
    b1 - buzzer1
    p - person
    g - greenled
    r - redled
    m - message)

(:init

    (off3 b)
    (at-buzzer b p)

    (off4 b1 )
    (at-buzzer1 b1 p)

    (off5 g )
    (at-greenled g p)

    (off6 r )
    (at-redled r p)

    ;movement ir sesnsor1 for entering
    (= (movement_value) 1)
    (= (movement p) 0)

    ; body temperature at the gate
    (= (bodytemp_limit) 35.0)
    (= (bodytemp p) 29.125)

    ;motion ir sesnsor 2 at the gate
    (= (motion_value) 1)
    (= (motion p) 0)

)

(:goal

    (and
          (bodytempcheck-performed)
          (employee-detected)
    ))

)