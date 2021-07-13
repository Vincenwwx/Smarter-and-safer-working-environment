(define (domain office)
  (:requirements   :strips  :typing  :negative-preconditions :disjunctive-preconditions :fluents :equality :conditional-effects)
  (:types
   buzzer buzzer1 person message  - object
   )
   
    (:predicates
         
          (bodytempcheck-performed)
          (person-detected)
          (off3 ?b - buzzer)
          (off4 ?b1 - buzzer1)
          (at-buzzer ?b - buzzer ?p - person)
          (at-buzzer1 ?b1 - buzzer1 ?p - person)
          (send ?m - message)     
    )

   (:functions
    
	  
	  (bodytemp ?p - person)
	  (motion ?p - person)
	  (bodytemp_limit)
	  (motion_value)
   )
   
    ; automatic bodytemp check in front of the office



    (:action switchoff_buzzer
        :parameters (?b - buzzer ?p - person ?m - message)
        :precondition (and (off3 ?b) (<(bodytemp ?p) (bodytemp_limit))) 
        :effect (and(not(off3 ?b)) (send ?m) (bodytempcheck-performed))
     )
   
     (:action switchon_buzzer
        :parameters (?b - buzzer ?p - person ?m - message)
        :precondition (or (not(off3 ?b)) (>(bodytemp ?p) (bodytemp_limit)))
        :effect (and (off3 ?b) (send ?m) (bodytempcheck-performed))
     )    

     ; ir sesnsor to detect person movement

    (:action switchoff_buzzer1
        :parameters (?b1 - buzzer1 ?p - person ?m - message)
        :precondition (and (off4 ?b1) (<(motion ?p) (motion_value))) 
        :effect (and(not(off4 ?b1)) (send ?m) (person-detected))
     )
   
     (:action switchon_buzzer1
        :parameters (?b1 - buzzer1 ?p - person ?m - message)
        :precondition (or (not(off4 ?b1)) (>=(motion ?p) (motion_value)))
        :effect (and (off4 ?b1) (send ?m) (person-detected))
     )    
)
